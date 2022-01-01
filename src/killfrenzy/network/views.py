from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from connections.models import *

def index(request):
    edges = Edge.objects.all()
    pps = {}
    mbps = {}
    cpu_load = {}

    for edge in edges:
        stats = Edge_Stats.objects.filter(edge_id=edge).latest('id')
        tot_pps = 0
        tot_mbps = 0
        
        if stats is not None:
            for k, v in stats.__dict__.items():
                if "pckts_ps" in k:
                    tot_pps = tot_pps + int(v)
                elif "bytes_ps" in k:
                    tot_mbps = tot_mbps + int((int(v) / 1e6))

        pps[edge.id] = tot_pps
        mbps[edge.id] = tot_mbps
        cpu_load[edge.id] = stats.cpu_load

    ctx = {"edges": edges, "pps": pps, "mbps": mbps, "cpu_load": cpu_load}

    return render(request, 'network/index.html', ctx)

def view_edge(request, edge_id):
    edge = get_object_or_404(Edge, id=edge_id)


    return render(request, 'network/view_edge.html', {"edge": edge})