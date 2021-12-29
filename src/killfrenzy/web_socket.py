from background_task import background

from connections.models import Connection, Whitelist, Blacklist, Port_Punch

import asyncio
import websockets

import json

async def handler(client):
    while True:
        print("Handling new client " + client.remote_address + ":" + str(client.remote_port) + "...")
        async for data in client:
            info = json.loads(data)

            ret = {}

            try:
                Connection.objects.get(bind_ip=client.remote_address)
            except websockets.DoesNotExist:
                ret["code"] = 404
                ret["type"] = "NotAuthorized"
                ret["Message"] = "Not authorized (not in connections list)"

                await client.send(json.dumps(ret))

            if info["type"] is None:
                continue

            if info["data"] is None:
                continue

async def start_server():
    async with websockets.serve(handler, "0.0.0.0", 8002):
        print("Web socket listening on port 8002...")
        await asyncio.Future()

@background(schedule=10)
def task_start():
    asyncio.run(start_server())