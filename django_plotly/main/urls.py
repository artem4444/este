from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('plots/', views.plot_page, name='plots'),

]
