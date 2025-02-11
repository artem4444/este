from django.urls import path
from . import views
from .views import example_data


urlpatterns = [
    path('', views.index, name='index'),
    path('plots/', views.plot_page, name='plots'),


    path('api/data/', example_data, name='example_data'),
    # When the browser or frontend (React) makes a GET request to this URL:
    # it triggers example_data(request), which returns a JSON response

]
