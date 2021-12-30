from connections.models import Edge, Edge_Settings, Edge_Stats, Connection, Connection_Stats, Whitelist, Blacklist, Port_Punch

import asyncio
import threading
from asgiref.sync import sync_to_async
from itertools import chain

import websockets
import json

conns = []

@sync_to_async
def get_edge(ip):
    return Edge.objects.filter(ip=ip).first()

@sync_to_async
def get_edge_settings(edge):
    return Edge_Settings.objects.filter(edge_id=edge.id).first()

@sync_to_async
def get_connections():
    return list(Connection.objects.all().values_list('enabled', 'bind_ip', 'bind_port', 'dest_ip', 'dest_port', 'udp_rl_bl', 'udp_rl_pps', 'udp_rl_bps', 'tcp_rl_bl', 'tcp_rl_pps', 'tcp_rl_bps', 'icmp_rl_bl', 'icmp_rl_pps', 'icmp_rl_bps', 'syn_rl_bl', 'syn_rl_pps', 'syn_rl_bps', 'a2s_info_enabled', 'a2s_info_cache_time'))

@sync_to_async
def get_whitelist():
    return list(Whitelist.objects.all().values_list('prefix', flat=True))

@sync_to_async
def get_blacklist():
    return list(Blacklist.objects.all().values_list('prefix', flat=True))

@sync_to_async
def get_port_punch():
    return list(Port_Punch.objects.all().values('ip', 'port'))

def to_dict(instance):
    opts = instance._meta
    data = {}

    for f in chain(opts.concrete_fields, opts.private_fields):
        data[f.name] = f.value_from_object(instance)

    for f in opts.many_to_many:
        data[f.name] = [i.id for i in f.value_from_object(instance)]

    return data

async def prepare_and_send_data(update_type="full_update", edge=None, settings=None, connections=None, whitelist=None, blacklist=None, port_punch=None):
    edges = list()

    # If we have one edge, just insert the one.
    if edge is not None:
        edges.append(edge)
    else:
        # Loop through all open connections and add to list.
        for i in conns:
            edges.append(i)

    i = 0

    # Loop through all edges.
    for edge_conn in edges:
        if edge_conn is None:
            print("prepare_and_send_data() :: Edge #" + str(i) + " is none.")

            continue

        print("Found edge for " + update_type)

        # Retrieve IP and port.
        ip = edge_conn.remote_address[0]
        port = edge_conn.remote_address[1]

        print("Sending data with type " + update_type + " to " + ip + ":" + str(port) + "...")

        # Make sure the edge exists in our database.
        edge_obj = await get_edge(ip)

        if edge_obj is None:
            print("Found a connection that is already established, but not validated. Closing " + ip + ":" + str(port))

            await edge_obj.close()

            continue

        ret = {}

        # Set type.
        ret["type"] = update_type

        # Initialize data.
        ret["data"] = {}

        if settings is not None and len(settings) < 1:
            settings = await get_edge_settings(edge_obj)

        if settings is not None:
            # Convert to dictionary if not already.
            if type(settings) is not dict:
                settings = to_dict(settings)

            # Set main settings.
            if "interface" in settings:
                ret["data"]["interface"] = settings["interface"]
            
            # Only set if the edge IP is filled.
            if "edge_ip" in settings:
                if len(settings["edge_ip"]) > 1:
                    ret["data"]["edge_ip"] = settings["edge_ip"]
            
            if "force_mode" in settings:
                ret["data"]["force_mode"] = settings["force_mode"]

            if "socket_count" in settings:    
                ret["data"]["socket_count"] = settings["socket_count"]

            if "queue_is_static" in settings:
                ret["data"]["queue_is_static"] = settings["queue_is_static"]

            if "queue_id" in settings:    
                ret["data"]["queue_id"] = settings["queue_id"]

            if "zero_copy" in settings:    
                ret["data"]["zero_copy"] = settings["zero_copy"]

            if "need_wakeup" in settings:    
                ret["data"]["need_wakeup"] = settings["need_wakeup"]

            if "batch_size" in settings:
                ret["data"]["batch_size"] = settings["batch_size"]

            if "verbose" in settings:
                ret["data"]["verbose"] = settings["verbose"]

            if "calc_data" in settings:    
                ret["data"]["calc_data"] = settings["calc_data"]

            if "allow_all_edge" in settings:
                ret["data"]["allow_all_edge"] = settings["allow_all_edge"]
            
        # Handle new connections.
        if connections is not None and len(connections) < 1:
            connections = await get_connections()
        
        if connections is not None:
            if len(connections) > 0:
                ret["data"]["connections"] = []

                for c in connections:
                    ret["data"]["connections"].append(c)

        # Handle whitelist.
        if whitelist is not None and len(whitelist) < 1:
            whitelist = await get_whitelist()
        
        if whitelist is not None:
            if len(whitelist) > 0:
                ret["data"]["whitelist"] = []

                for w in whitelist:
                    ret["data"]["whitelist"].append(w[:])

        # Handle blacklist.
        if blacklist is not None and len(blacklist) < 1:
            blacklist = await get_blacklist()
        
        if blacklist is not None:
            if len(blacklist) > 0:
                ret["data"]["blacklist"] = []

                for b in blacklist:
                    ret["data"]["blacklist"].append(b)

        # Handle port punch.
        if port_punch is not None and len(port_punch) < 1:
            port_punch = await get_port_punch()
        
        if port_punch is not None:
            if len(port_punch) > 0:
                ret["data"]["port_punch"] = []

                for p in port_punch:
                    ret["data"]["port_punch"].append(p)

        print("Sending to " + ip + ":" + str(port) + " => " + json.dumps(ret))
        await edge_conn.send(json.dumps(ret))
        
        i = i + 1

async def handler(client):
    conns.append(client)
    ip = client.remote_address[0]
    port = client.remote_address[1]

    while True:
        edge = None

        if client.open is False:
            print("Connection from " + ip + ":" + str(port) + " ended.")
            conns.remove(client)

            if edge is not None:
                edge.status = False
                edge.save()

            break

        print("Handling new client " + ip + ":" + str(port) + "...")

        try:
            async for data in client:
                info = json.loads(data)

                ret = {}

                edge = await get_edge(ip)

                if edge is None:
                    print("Found invalidated request from " + ip + ":" + str(port))

                    ret["code"] = 404
                    ret["type"] = "NotAuthorized"
                    ret["message"] = "Not authorized (not in connections list)"

                    await client.send(json.dumps(ret))
                    await client.close()

                    break

                # Make sure we have valid data.
                if "type" not in info:
                    continue

                if info["type"] == "full_update":
                    await prepare_and_send_data("full_update", client, settings={}, connections=[], whitelist=[], blacklist=[], port_punch=[])
                if info["type"] == "settings":
                    await prepare_and_send_data("settings", client, settings={})
                elif info["type"] == "connections":
                    await prepare_and_send_data("connections", client, connections=[])
                elif info["type"] == "whitelist":
                    await prepare_and_send_data("whitelist", client, whitelist=[])
                elif info["type"] == "blacklist":
                    await prepare_and_send_data("blacklist", client, blacklist=[])
                elif info["type"] == "port_punch":
                    await prepare_and_send_data("port_punch", client, port_punch=[])
                
                elif info["type"] == "push_stats":
                    if "data" not in info:
                        continue

                    stat_data = info["data"]
                    
                    stat = Edge_Stats(edge_id=edge.id, bla_pckts=stat_data["bla_pckts"], bla_pckts_ps=stat_data["bla_pckts_ps"], bla_bytes=stat_data["bla_bytes"], bla_bytes_ps=stat_data["bla_bytes_ps"], whi_pckts=stat_data["whi_pckts"], whi_pckts_ps=stat_data["whi_pckts_ps"], whi_bytes=stat_data["whi_bytes"], whi_bytes_ps=stat_data["whi_bytes_ps"], blo_pckts=stat_data["blo_pckts"], blo_pckts_ps=stat_data["blo_pckts_ps"], blo_bytes=stat_data["blo_bytes"], blo_bytes_ps=stat_data["blo_bytes_ps"], pass_pckts=stat_data["pass_pckts"], pass_pckts_ps=stat_data["pass_pckts_ps"], pass_bytes=stat_data["pass_bytes"], pass_bytes_ps=stat_data["pass_bytes_ps"], fwd_pckts=stat_data["fwd_pckts"], fwd_pckts_ps=stat_data["pass_pckts_ps"], fwd_bytes=stat_data["pass_bytes"], fwd_bytes_ps=stat_data["pass_bytes_ps"], fwdo_pckts=stat_data["fwdo_pckts"], fwdo_pckts_ps=stat_data["fwdo_pckts_ps"], fwdo_bytes=stat_data["fwdo_bytes"], fwdo_bytes_ps=stat_data["fwdo_bytes_ps"], bad_pckts=stat_data["bad_pckts"], bad_pckts_ps=stat_data["bad_pckts_ps"], bad_bytes=stat_data["bad_bytes"], bad_bytes_ps=stat_data["bad_bytes_ps"], a2rp_pckts=stat_data["a2rp_pckts"], a2rp_pckts_ps=stat_data["a2rp_pckts_ps"], a2rp_bytes=stat_data["a2rp_bytes"], a2rp_bytes_ps=stat_data["a2rp_bytes_ps"], a2rs_pckts=stat_data["a2rs_pckts"], a2rs_pckts_ps=stat_data["a2rs_pckts_ps"], a2rs_bytes=stat_data["a2rs_bytes"], a2rs_bytes_ps=stat_data["a2rs_bytes_ps"], dro_pckts=stat_data["dro_pckts"], dro_pckts_ps=stat_data["dro_pckts_ps"], dro_bytes=stat_data["dro_bytes"], dro_bytes_ps=stat_data["dro_bytes_ps"], drc_pckts=stat_data["drc_pckts"], drc_pckts_ps=stat_data["drc_pckts_ps"], drc_bytes=stat_data["drc_bytes"], drc_bytes_ps=stat_data["drc_bytes_ps"])
                    stat.save()
                elif info["type"] == "push_port_punch":
                    if "data" not in info:
                        continue

                    pp_data = info["data"]

                    pp = Port_Punch(ip=pp_data["ip"], port=pp_data["port"])
                    pp.save()

        except websockets.exceptions.ConnectionClosedError:
            print("Closing connection...")
    
async def start_server():
    async with websockets.serve(handler, "0.0.0.0", 8003):
        print("Web socket listening on port 8003...")
        await asyncio.Future()

def thread_start():
    asyncio.run(start_server())

def task_start():
    t = threading.Thread(target=thread_start)
    t.setDaemon(True)
    t.start()