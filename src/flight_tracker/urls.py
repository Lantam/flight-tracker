from django.urls import include, path
from map.views import index, process_request, add_filter, remove_filter
from map.api_urls import router


urlpatterns = [
    path('', index, name='index'),
    path('process-request', process_request, name='process_request'),
    path('add-filter', add_filter, name='add_filter'),
    path('remove-filter', remove_filter, name='remove_filter'),
    path('api/', include(router.urls)),
]
