from django.urls import include, path
from map.views import index, get_zoom_level_bounds
from map.api_urls import router


urlpatterns = [
    path('', index, name='index'),
    path('get_zoom_level_bounds', get_zoom_level_bounds, name='get_zoom_level_bounds'),
    path('api/', include(router.urls)),
]
