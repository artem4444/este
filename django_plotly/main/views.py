from django.shortcuts import render
from django.http import HttpResponse
from .plots.plotly_plots import generate_iris_scatter_plot, PlotlyPlots
import plotly.graph_objects as go
import plotly.utils
import json
import logging

import subprocess
import threading
import os
import time


######
#for React app:
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET']) #turns a function into an API view: only allows HTTP GET requests 
#@permission_classes([IsAuthenticated])  # Only logged-in users can access: not to be seen from browsered url
def example_data(request):
    return Response({"message": "Hello from Django API!"})


######




def index(request):
    # Get the Plotly graph HTML from the helper function:
    #Convert the plot to HTML for embedding: function itself generates html file in runtime: .html is not stored anywhere
    #{{ graph_html|safe }} embeds this generated html code into the index.html web page
    graph_html = generate_iris_scatter_plot()
    
    #calls html template with {graph_html} django template as parameter
    return render(request, 'main/index.html', {'graph_html': graph_html})
    
def plot_page(request):
    
    #plots_data = plots_orchestrator()

    # plotly_plots = PlotlyPlots()
    # plots_data = plotly_plots.plots_orchestrator()

    '''with current plots.html (containing css inside it):
    i can code any amount of plots to be rendered 
    in this page and they will be rendered 
    1 or 2 in a row,depending on resolution, 
    one by one going down

    plots.html renders data from json encoded by json.dumps with fig containing all parameters regarding plotly plot:
    fig - json.dump - plots_orchestrator.create_scatter_plot{} - plots_data - js script in html template
    '''
    json_file = '/home/artem/Mosaic/este/django_plotly/main/plots/plots.json'
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    
    plotly_plots = PlotlyPlots(json_data=data)
    plots_data = plotly_plots.plots_orchestrator()

    return render(request, 'main/plots.html', {'plots_data': plots_data})
    

