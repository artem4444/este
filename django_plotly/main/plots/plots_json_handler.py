import json
import plotly.graph_objects as go

class PlotsJSON:
    def __init__(self):
        self.data = {}

    def save_data(self, filename: str) -> None:
        """
        Save all plot data to a JSON file.
        
        Args:
            filename (str): The name of the file to save the data.
        """
        try:
            with open(filename, 'w') as f:
                json.dump(self.data, f, indent=4)
        except Exception as e:
            raise IOError(f"Failed to save data to '{filename}': {e}")

    def load_data(self, filename: str) -> dict:
        """
        Load all plot data from a JSON file.
        
        Args:
            filename (str): The name of the file to load the data from.
        
        Returns:
            dict: The loaded plot data.
        
        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file contains invalid JSON.
        """
        try:
            with open(filename, 'r') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"The file '{filename}' does not exist.")
        except json.JSONDecodeError:
            raise ValueError(f"The file '{filename}' is not a valid JSON.")
        return self.data

    def add_plot_data(self, plot_name: str, plot_dict: dict, overwrite: bool = False) -> None:
        """
        Add a new plot's dictionary to the data.
        
        Args:
            plot_name (str): The name of the plot.
            plot_dict (dict): The dictionary containing plot data.
            overwrite (bool): If True, overwrite existing plot data.
        
        Raises:
            ValueError: If the plot data is invalid or already exists and overwrite is False.
        """
        self.validate_plot_data(plot_dict)
        if plot_name in self.data and not overwrite:
            raise ValueError(f"Plot '{plot_name}' already exists. Use overwrite=True to replace it.")
        self.data[plot_name] = plot_dict

    def update_plot_data(self, plot_name: str, updated_dict: dict) -> None:
        """
        Update an existing plot's data.
        
        Args:
            plot_name (str): The name of the plot.
            updated_dict (dict): The updated dictionary to merge into the existing plot.
        
        Raises:
            KeyError: If the plot does not exist.
        """
        if plot_name not in self.data:
            raise KeyError(f"Plot '{plot_name}' does not exist.")
        self.data[plot_name].update(updated_dict)

    def delete_plot_data(self, plot_name: str) -> None:
        """
        Delete a specific plot from the data.
        
        Args:
            plot_name (str): The name of the plot.
        
        Raises:
            KeyError: If the plot does not exist.
        """
        if plot_name in self.data:
            del self.data[plot_name]
        else:
            raise KeyError(f"Plot '{plot_name}' does not exist.")

    def get_plot_data(self, plot_name: str) -> dict:
        """
        Retrieve a specific plot's data.
        
        Args:
            plot_name (str): The name of the plot.
        
        Returns:
            dict: The plot data.
        
        Raises:
            KeyError: If the plot does not exist.
        """
        if plot_name in self.data:
            return self.data[plot_name]
        else:
            raise KeyError(f"Plot '{plot_name}' does not exist.")

    def list_plots(self) -> list:
        """
        List all available plots.
        
        Returns:
            list: A list of plot names.
        """
        return list(self.data.keys())

    def create_plot(self, plot_name: str) -> None:
        """
        Render a Plotly plot based on stored data.
        
        Args:
            plot_name (str): The name of the plot to render.
        
        Raises:
            KeyError: If the plot does not exist.
            ValueError: If the plot type is not supported.
        """
        if plot_name not in self.data:
            raise KeyError(f"No data found for plot: {plot_name}")

        plot_info = self.data[plot_name]
        plot_type = plot_info.get('type', 'scatter')  # Default to scatter

        fig = go.Figure()
        trace_mapping = {
            'line': go.Scatter(mode='lines'),
            'scatter': go.Scatter(mode='markers'),
            'bar': go.Bar(),
            # Add other plot types as needed
        }

        if plot_type not in trace_mapping:
            raise ValueError(f"Unsupported plot type: {plot_type}")

        trace = trace_mapping[plot_type]
        fig.add_trace(trace.update(
            x=plot_info['x_data'],
            y=plot_info['y_data'],
            **plot_info.get('properties', {})
        ))

        # Update layout properties
        fig.update_layout(
            title=plot_info.get('properties', {}).get('title', 'Plot'),
            xaxis_title=plot_info.get('properties', {}).get('xlabel', 'X Axis'),
            yaxis_title=plot_info.get('properties', {}).get('ylabel', 'Y Axis'),
        )

        fig.show()

    @staticmethod
    def validate_plot_data(plot_dict: dict) -> None:
        """
        Validate the structure and content of plot data.
        
        Args:
            plot_dict (dict): The dictionary to validate.
        
        Raises:
            ValueError: If the plot data is invalid.
        """
        if 'x_data' not in plot_dict or 'y_data' not in plot_dict:
            raise ValueError("Plot data must contain 'x_data' and 'y_data'.")
        if len(plot_dict['x_data']) != len(plot_dict['y_data']):
            raise ValueError("'x_data' and 'y_data' must be of equal length.")

# Example usage
if __name__ == "__main__":
    # Create sample data
    x_data = [1, 2, 3, 4, 5]
    y_data = [2, 4, 6, 8, 10]

    # Initialize handler
    handler = PlotsJSON()

    # Add plot data with properties
    handler.add_plot_data(
        'example_plot',
        {
            'x_data': x_data,
            'y_data': y_data,
            'type': 'line',
            'properties': {
                'title': 'Example Plot',
                'xlabel': 'X Axis',
                'ylabel': 'Y Axis',
                'line_color': 'blue',
            }
        }
    )

    # Save to JSON file
    handler.save_data('plots.json')

    # Load from JSON file
    handler.load_data('plots.json')

    # Create plot from loaded data
    handler.create_plot('example_plot')
