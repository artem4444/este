from django.urls import path
from . import views
from .views import example_data , c4_diagram


urlpatterns = [
    path('', views.index, name='index'),
    path('plots/', views.plot_page, name='plots'),


    path('api/data/', example_data, name='example_data'),
    # When the browser or frontend (React) makes a GET request to this URL:
    # it triggers example_data(request), which returns a JSON response
    path('c4/', c4_diagram, name='c4_diagram'),
]
