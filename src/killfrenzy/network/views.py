from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from connections.models import *

def index(request):
    edges = Edge.objects.all()
    pps = {}
    mbps = {}
    cpu_load = {}
    xdp_status = {}


    for edge in edges:
        if edge is None:
            continue
        
    ctx = {"edges": edges, "pps": pps, "mbps": mbps, "cpu_load": cpu_load, "xdp_status": xdp_status}

    return render(request, 'network/index.html', ctx)

def view_edge(request, edge_id):
    edge = get_object_or_404(Edge, id=edge_id)


    return render(request, 'network/view_edge.html', {"edge": edge})