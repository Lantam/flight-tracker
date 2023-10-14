from django.urls import path
from map import views


urlpatterns = [
    path('', views.index, name='index'),
    path('add_all_markers', views.add_all_markers, name='add_all_markers'),
]
