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



# iFrame: modular Frontend
embedded inside of streamlit elements
in iframe: apps' streaming players, js-html rendered content

# Django-React
this React container will work with any web framework as long as the framework:
-Exposes an API endpoint that React can call
-Uses standard HTTP requests (REST or GraphQL)

from local react development i will copy everything necessary into encapsulated_react container, that is based on official docker image of nodejs-react 

In production, your React app can run as a distinct microservice separate from Django, communicating only through API calls. This decoupled architecture is commonly used in microservices-based deployments


# React endpoints to web framework:

1. React web page to web framework
connection to views.py:
- api get requests

2. web page elements connection to logic
~hooks to url address of backend container


# React development
#### locally hosted react app build:
sudo apt update
sudo apt install nodejs npm

npm install -g create-react-app


npm config set prefix /home/artem/.npm-global

npx create-react-app react_grid_gui --legacy-peer-deps

#### react app running:
cd frontend_react
npm start

#### React Grid Layout
(npm install react-grid-layout)

1. Browser loads index.html, which contains:
<div id="root"></div>
2. index.js mounts <App /> into <div id="root">.
3. App.js renders GridLayout.js inside it.
4. GridLayout.js loads and displays the draggable grid.
5. The browser updates dynamically when you move or resize the boxes.

#### fully React Grid Layout-based UI 
=where every element (menus, content, buttons, forms, etc.) is inside a grid box

###### GridLayout.js is the root layout of the app
controlling if a grid element is static or adjustable: '... static: true/false ...'

App.css contains styling of elements of the layout

#### add something inside grid-element
example:
how to add something inside top navbar: GridLayout.js: 
```
<div key="navbar" ...
  here
</div>
```
add responsiveness in GridLayout.css

if i will add anything into react-grid-layout: it will act as if borders of the grid-box would be borders of a browser window


# d3.js
D3.js runs entirely on the client side in the browser
