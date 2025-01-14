from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('plots/', views.plot_page, name='plots'),
    path('multi_player/', views.multi_player_view, name='multi_player'),
    path('streamlit/', views.streamlit_view, name='streamlit'),
]
