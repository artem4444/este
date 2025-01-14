from django.shortcuts import render
from django.http import HttpResponse
import streamlit.web.bootstrap as bootstrap
from .plots.plotly_plots import generate_iris_scatter_plot, PlotlyPlots
import plotly.graph_objects as go
import plotly.utils
import json
from .streamlit.streamlit_app import run_streamlit_app
import logging

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

def streamlit_view(request):
    # Pass the Streamlit server URL to the template
    streamlit_url = "http://localhost:8501"
    return render(request, 'main/streamlit.html', {'streamlit_url': streamlit_url})

def launch_streamlit():
    import streamlit.web.bootstrap as bootstrap
    from streamlit.web.cli import main
    
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    flag_options = {
        "server.address": "localhost",
        "server.port": 8501,
        "browser.serverAddress": "localhost",
        "server.headless": True,
        "server.runOnSave": True,
        "global.developmentMode": False,
    }
    
    logger.info("Starting Streamlit server...")
    try:
        bootstrap.run(run_streamlit_app, "", flag_options=flag_options)
        logger.info("Streamlit server started successfully")
    except Exception as e:
        logger.error(f"Error starting Streamlit server: {str(e)}")
        raise