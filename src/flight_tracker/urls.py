from django.urls import include, path
from map.views import index, process_request, clear_filter
from map.api_urls import router


urlpatterns = [
    path('', index, name='index'),
    path('process-request', process_request, name='process_request'),
    path('clear-filter', clear_filter, name='clear_filter'),
    path('api/', include(router.urls)),
]
