# streamlit_apps/streamlit_app.py
import streamlit as st
from main.plots.plotly_plots import PlotlyPlots
import json
import os
import datetime
from main.streamlit_apps.plotly_dashboard import PlotlyDashboard
from main.streamlit_apps.user_chat import UserChat


def main():
    st.set_page_config(layout="wide")
    
    # Add custom CSS to reduce left padding
    st.markdown("""
        <style>
        .block-container {
            padding-left: 2rem;
            padding-right: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Initialize chat first
    chat = UserChat()
    # Pass chat interface to dashboard
    dashboard = PlotlyDashboard(chat)

    # Create three columns layout with specified proportions
    # 2/5 : 1/5 : 1/5 (total = 4/5 of page width)
    chat_col, plot_col1, plot_col2 = st.columns([2, 1, 1])

    # Render HuggingFace chat interface in left column (2/5 width)
    UserChat.render_huggingface_chat(chat_col)

    # Render first plot in middle column (1/5 width)
    with plot_col1:
        st.markdown("### Plot 1")
        dashboard.render_single_plot(plot_index=0)

    # Render second plot in right column (1/5 width)
    with plot_col2:
        st.markdown("### Plot 2")
        dashboard.render_single_plot(plot_index=1)


if __name__ == "__main__":
    main()
