# llm queries
Anthropic Claude3.5 Sonnet API


# Node(Agent)
superclass for all nodes

llm_query provides API calling functionality 


# container.django_plotly

``` bash: routine: venv, django start:

cd django_plotly
source venv_django_plotly/bin/activate

python manage.py runserver

```
textual file-structure representation: tree django_plotly/main/

simple set of plotly diagrams- all UI will be done when MVP is ready (ninu)


# plots
with current plots.html (containing css inside it):
i can code any amount of plots to be rendered 
in this page and they will be rendered 
1 or 2 in a row,depending on resolution, 
one by one going down

plots.html renders data from json encoded by json.dumps with fig containing all parameters regarding plotly plot:
fig - json.dump - plots_orchestrator.create_scatter_plot{} - plots_data - js script in html template

we use single JSON for all plots in our page
JSON serves like a runtime hub for all our plots


## Plotly Plots
plots are rendered in the same order as they are in the JSON

    @staticmethod #belongs to the class itself rather than to instances of the class
    #code would always work same way without @staticmethod , just little bit slower

    if __name__ == "__main__":
    can always be used for module test purpose: doesn't affect program's runtime at all



## PlotsJSON():
1. handle processing data for all existing Plotly plots: connect plots' python dictionaries into single JSON file storing them all
2. fully service the Plots JSON

*PlotsJSON initialises plots.json itself and serves it's runtime while it itself is running*




###### save_data
save plot data to JSON file
###### load_data
load plot data from JSON file


###### add_plot_data
allows you to store multiple plots in a single JSON file:

**kwargs : add more plotly parameters in any order if need
plotly will retrieve parameters by parameters unique keys

###### create_plot
this create_plot function takes python dictionary from module that called it in the first place and initializes plot in the JSON, adding data from python dictionary to it


# plots.json - psql
.html-views.py-PlotlyPlots-PlotsJSON-plots.json-*psql*

psql servicing class, that different part of programm will be able to use for messaging/storing using psql through JSON: their native storing/communicating format

single for all apps

PostgreSQL's LISTEN/NOTIFY feature replaces custom python functions that would regularly check selected psql tables for udates

*JSON content doen't matter for psql-handler functionality*: /psql_handler.PSQL_Handler can be used with any app


# streamlit gui
chat, plots, players

#### streamlit apps in parallel
write port of needed app in here : streamlit_url = "http://localhost:8501". the rest of apps will run in their own threads

when hosted in container:
```python
streamlit_url = "http://192.168.1.100:8501"  # Replace with actual IP and port
```