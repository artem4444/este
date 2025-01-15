from django.shortcuts import render
from django.http import HttpResponse
import streamlit.web.bootstrap as bootstrap
from .plots.plotly_plots import generate_iris_scatter_plot, PlotlyPlots
import plotly.graph_objects as go
import plotly.utils
import json
from .streamlit_apps.streamlit_app import main
import logging

import subprocess
import threading
import os
import time


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
    


def multi_player_view(request):
    # URLs for cloud-hosted players
    player_urls = [
        "https://cloud-player1.com",
        "https://cloud-player2.com",
        "https://cloud-player3.com"
    ]
    return render(request, 'main/multi_player.html', {'player_urls': player_urls})


# def streamlit_view(request):
#     # Start Streamlit in a separate thread
#     import threading
    
#     # Only start the thread if Streamlit isn't already running
#     if not any(t.name == "StreamlitThread" for t in threading.enumerate()):
#         thread = threading.Thread(target=launch_streamlit, name="StreamlitThread")
#         thread.daemon = True
#         thread.start()
    
#     # Wait a short time for Streamlit to start
#     import time
#     time.sleep(2)
    
#     # Pass the Streamlit server URL to the template
#     streamlit_url = "http://localhost:8501"
#     return render(request, 'main/streamlit.html', {'streamlit_url': streamlit_url})

# def launch_streamlit():
#     import streamlit.web.bootstrap as bootstrap
#     from streamlit.web.cli import main
#     import streamlit.bootstrap as bootstrap
#     import sys
#     from streamlit.web import cli as stcli
    
#     sys.argv = ["streamlit", "run", "your_streamlit_app.py"]
#     sys.exit(stcli.main())
#     # Set up logging
#     logging.basicConfig(level=logging.INFO)
#     logger = logging.getLogger(__name__)
    
#     flag_options = {
#         "server.address": "localhost",
#         "server.port": 8501,
#         "browser.serverAddress": "localhost",
#         "server.headless": True,
#         "server.runOnSave": True,
#         "global.developmentMode": False,
#     }
    
#     logger.info("Starting Streamlit server...")
#     try:
#         bootstrap.run(run_streamlit_app, "", flag_options=flag_options)
#         logger.info("Streamlit server started successfully")
#     except Exception as e:
#         logger.error(f"Error starting Streamlit server: {str(e)}")
#         raise


def launch_streamlit():
    try:
        # Get the path to streamlit_app.py in the streamlit_apps directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        streamlit_app_path = os.path.join(current_dir, 'streamlit_apps', 'streamlit_app.py')
        
        if not os.path.exists(streamlit_app_path):
            raise FileNotFoundError(f"Streamlit app not found at: {streamlit_app_path}")

        print(f"Starting Streamlit with app at: {streamlit_app_path}")
        
        # Set the working directory to the streamlit_apps directory
        # This ensures relative imports and file paths work correctly
        working_dir = os.path.dirname(streamlit_app_path)
        
        # Launch Streamlit as a subprocess
        process = subprocess.Popen([
            'streamlit',
            'run',
            streamlit_app_path,
            '--server.port=8501',
            '--server.address=localhost'
        ], 
        cwd=working_dir,  # Set working directory
        env={**os.environ, 'PYTHONPATH': os.path.dirname(current_dir)}  # Add project root to PYTHONPATH
        )
        
        return process
        
    except Exception as e:
        print(f"Error launching Streamlit: {str(e)}")
        raise

def streamlit_view(request):
    # Start Streamlit in a separate thread if it's not already running
    if not any(t.name == "StreamlitThread" for t in threading.enumerate()):
        thread = threading.Thread(target=launch_streamlit, name="StreamlitThread")
        thread.daemon = True
        thread.start()
    
    # Give Streamlit a moment to start
    time.sleep(2)
    
    # Pass the Streamlit server URL to the template
    streamlit_url = "http://localhost:8501"
    return render(request, 'main/streamlit.html', {'streamlit_url': streamlit_url})