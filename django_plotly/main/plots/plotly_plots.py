import plotly.express as px
import plotly.graph_objects as go
import json
import plotly 
from .plots_json_handler import PlotsJSON #it handles all interactions through JSON:
#this module only works with 'clean' python dictionaries
#json file is created in runtime, so as python dictionary 


'''
for index.html view:
'''
def generate_iris_scatter_plot():
    # Generate a Plotly scatter plot using the Iris dataset
    df = px.data.iris()  # Using Plotly's built-in Iris dataset
    fig = px.scatter(df, x='sepal_width', y='sepal_length', color='species', title='Iris Dataset')
    #Convert the plot to HTML for embedding: function itself generates html file in runtime: .html is not stored anywhere
    #this {{ graph_html|safe }} embeds this generated html code into the web page
    return fig.to_html(full_html=False)




'''
for plots.html view:
'''

import json
import plotly.graph_objects as go
import plotly.utils

class PlotlyPlots:
    def __init__(self, json_data=None):
        """
        Initialize with optional JSON data.
        Args:
            json_data (dict): Data loaded from a JSON file.
        """
        self.plots_data = []
        self.json_data = json_data or []

    def plots_orchestrator(self):
        """
        Main function that processes JSON data and generates plots.
        Returns:
            list: A list of dictionaries containing plotly figures and descriptions.
        """
        if not self.json_data:
            raise ValueError("No JSON data provided.")
        
        for index, plot_info in enumerate(self.json_data, start=1):
            plot_type = plot_info.get("type")
            if plot_type == "scatter":
                self.plots_data.append(self.create_scatter_plot(index, plot_info))
            elif plot_type == "bar":
                self.plots_data.append(self.create_bar_plot(index, plot_info))
            elif plot_type == "line":
                self.plots_data.append(self.create_line_plot(index, plot_info))
            else:
                raise ValueError(f"Unsupported plot type: {plot_type}")
        
        return self.plots_data

    @staticmethod
    def apply_common_layout(fig):
        """Apply common styling to all plots."""
        fig.update_layout(
            paper_bgcolor='black',
            plot_bgcolor='black',
            font_color='white',
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis=dict(
                gridcolor='#444',
                zerolinecolor='#444',
            ),
            yaxis=dict(
                gridcolor='#444',
                zerolinecolor='#444',
            ),
        )
        return fig

    '''Plots:'''

    def create_scatter_plot(self, index, plot_info):
        """Create a scatter plot using data from JSON."""
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=plot_info.get("x_data", []),
            y=plot_info.get("y_data", []),
            mode=plot_info.get("mode", "markers"),
            marker=plot_info.get("marker", {"size": 10, "color": "magenta"})
        ))

        fig = self.apply_common_layout(fig)

        return {
            'plot': json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder),
            'description': plot_info.get("description", f"Scatter plot #{index}")
        }

    def create_bar_plot(self, index, plot_info):
        """Create a bar plot using data from JSON."""
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=plot_info.get("x_data", []),
            y=plot_info.get("y_data", []),
            marker_color=plot_info.get("marker_color", "magenta")
        ))

        fig = self.apply_common_layout(fig)

        return {
            'plot': json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder),
            'description': plot_info.get("description", f"Bar plot #{index}")
        }

    def create_line_plot(self, index, plot_info):
        """Create a line plot using data from JSON."""
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=plot_info.get("x_data", []),
            y=plot_info.get("y_data", []),
            mode=plot_info.get("mode", "lines+markers"),
            line=plot_info.get("line", {"color": "magenta", "width": 2})
        ))

        fig = self.apply_common_layout(fig)

        return {
            'plot': json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder),
            'description': plot_info.get("description", f"Line plot #{index}")
        }

# Example Usage with JSON Data
if __name__ == "__main__":
    # Load JSON data
    json_file = 'plots.json'
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    
    plotly_plots = PlotlyPlots(json_data=data)
    plots_data = plotly_plots.plots_orchestrator()

