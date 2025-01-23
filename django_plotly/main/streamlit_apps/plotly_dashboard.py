import os
import json
import streamlit as st
from main.plots.plotly_plots import PlotlyPlots

class PlotlyDashboard:
    def __init__(self, chat_interface):
        self.current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.json_file = os.path.join(self.current_dir, 'plots', 'plots.json')
        self.chat_interface = chat_interface  # Store reference to chat interface

    def load_plot_data(self):
        try:
            with open(self.json_file, 'r') as f:
                data = json.load(f)
            return data
        except Exception as e:
            st.error(f"Error loading plot data: {str(e)}")
            return None

    def handle_plot_interaction(self, plot_name, action):
        """Handle plot interactions and send messages to chat"""
        if action == "update":
            self.chat_interface.publish_bot_message(
                f"I've updated the {plot_name} plot with your specifications.",
                plot_updates={"plot": plot_name, "action": "update"}
            )
        elif action == "show":
            self.chat_interface.publish_bot_message(
                f"Here's the {plot_name} plot you requested.",
                plot_updates={"plot": plot_name, "action": "show"}
            )

    def render_plots(self):
        st.title("Plotly Plots Dashboard")
        try:
            data = self.load_plot_data()
            if data:
                plotly_plots = PlotlyPlots(json_data=data)
                plots_data = plotly_plots.plots_orchestrator()

                # Create tabs for each plot
                tabs = st.tabs([f"Plot {i+1}" for i in range(len(plots_data))])
                
                # Render each plot in its own tab
                for tab, plot_data in zip(tabs, plots_data):
                    with tab:
                        # Add a title or description at the top of the tab
                        st.markdown(f"### {plot_data.get('title', 'Plot')}")
                        
                        # Create columns for plot and description
                        plot_col, desc_col = st.columns([3, 1])
                        
                        with plot_col:
                            fig_dict = json.loads(plot_data['plot'])
                            st.plotly_chart(fig_dict, use_container_width=True)
                        
                        with desc_col:
                            st.markdown("#### Description")
                            st.write(plot_data['description'])
                            
                            # Add any interactive controls specific to this plot
                            st.markdown("#### Controls")
                            st.markdown("*Plot-specific controls can be added here*")
                    
        except Exception as e:
            st.error(f"Error processing plots: {str(e)}")
            print(f"Detailed error: {str(e)}")

    def render_single_plot(self, plot_index=0):
        """Render a single plot by index"""
        try:
            data = self.load_plot_data()
            if data:
                plotly_plots = PlotlyPlots(json_data=data)
                plots_data = plotly_plots.plots_orchestrator()
                
                if plot_index < len(plots_data):
                    plot_data = plots_data[plot_index]
                    
                    # Display plot title
                    st.markdown(f"#### {plot_data.get('title', 'Plot')}")
                    
                    # Display plot
                    fig_dict = json.loads(plot_data['plot'])
                    st.plotly_chart(fig_dict, use_container_width=True)
                    
                    # Display description
                    with st.expander("Plot Description"):
                        st.write(plot_data['description'])
                else:
                    st.warning("Plot index out of range")
                    
        except Exception as e:
            st.error(f"Error processing plot: {str(e)}")
            print(f"Detailed error: {str(e)}")