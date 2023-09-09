from django.urls import include, path
from rest_framework import routers
from map import views


urlpatterns = [
    path('', views.index, name='index'),
    path('add_all_markers', views.add_all_markers, name='add_all_markers'),
    path('get_response', views.get_response, name='get_response'),
]
