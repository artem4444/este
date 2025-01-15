# streamlit_apps/streamlit_app.py
import streamlit as st
from main.plots.plotly_plots import PlotlyPlots
import json
import os

def main():
    st.set_page_config(layout="wide")
    st.title("Plotly Plots Dashboard")

    try:
        # Get the path to plots.json
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        json_file = os.path.join(current_dir, 'plots', 'plots.json')
        
        # Load JSON data
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
                
    except Exception as e:
        st.error(f"Error loading or processing data: {str(e)}")
        print(f"Detailed error: {str(e)}")  # This will show in the server logs

if __name__ == "__main__":
    main()