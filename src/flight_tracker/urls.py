from django.urls import include, path
from map.views import index
from map.api_urls import router


urlpatterns = [
    path('', index, name='index'),
    path('api/', include(router.urls)),
]
