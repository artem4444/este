import streamlit as st
from ..plots.plotly_plots import PlotlyPlots
import json

def run_streamlit_app():
    st.set_page_config(layout="wide")
    st.title("Plotly Plots Dashboard")

    # Load JSON data
    json_file = 'main/plots/plots.json'  # Adjust path as needed
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    plotly_plots = PlotlyPlots(json_data=data)
    plots_data = plotly_plots.plots_orchestrator()

    # Create columns for plots (2 columns)
    cols = st.columns(2)
    
    # Display plots in columns
    for idx, plot_data in enumerate(plots_data):
        with cols[idx % 2]:
            # Parse the JSON string back to a dict
            fig_dict = json.loads(plot_data['plot'])
            # Create and display the figure
            st.plotly_chart(fig_dict, use_container_width=True)
            st.write(plot_data['description'])