from django.shortcuts import render
from django.utils.safestring import mark_safe
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
    


'''
with find_file i won't spend more computer power or time, than if it was BASE_DIR,
if search_path will be of same precision

easier to use modules from other apps
-when i will pack apps in containers: 
 functionality of tranfer of data between containers will need to be added
'''
def find_file(filename, search_path="/"):
    for root, _, files in os.walk(search_path):
        if filename in files:
            return os.path.join(root, filename)
    return None

def c4_diagram(request):
    js_file_path = find_file("c4.js", "/home/artem/Mosaic/este/d3_c4")  # Adjust search path as needed
        #\\wsl.localhost\Ubuntu-24.04\home\artem\Mosaic\este\d3_c4
    if not js_file_path:
        return render(request, "error.html", {"message": "c4.js not found"})

    with open(js_file_path, "r") as file:
        d3_js_code = file.read()

    return render(request, "c4_diagram.html", {"your_d3_js_code": mark_safe(d3_js_code)})