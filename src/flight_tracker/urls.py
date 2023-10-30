from django.urls import path
from map.views import index, add_all_markers


urlpatterns = [
    path('', index, name='index'),
    path('add_all_markers', add_all_markers, name='add_all_markers'),
]
