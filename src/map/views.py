from django.shortcuts import render
from map.forms import SearchForm
from map.models import Search
from django_redis import get_redis_connection
from json import loads
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def get_zoom_level_bounds(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.method == 'POST':
            data = loads(request.body.decode('utf-8'))
            zoom_level = data.get('zoom_level')
            bounds = data.get('bounds')

            end_data = add_markers(bounds=bounds, zoom_level=zoom_level)

            return JsonResponse(end_data, safe=False)
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')


def index(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            form.save()
            filter = Search.objects.last().location
            marker_data = add_markers(filter)
            return JsonResponse({'markers': marker_data})
    else:
        form = SearchForm()

    context = {'form': form, }
    return render(request, 'map.html', context)


def add_markers(filter=None, bounds=None, zoom_level=None):
    redis = get_redis_connection()
    api_data = redis.hgetall("cache")

    elevation_mapping = {
        1: 99999,
        2: 99999,
        3: 14000,
        4: 13000,
        5: 12000,
        6: 11000,
        7: 10000,
        8: 9000,
        9: 8000,
        10: 7000,
    }

    store = []

    for value in api_data.values():
        data = loads(value)

        if filter is not None and filter not in data.values():
            continue

        if bounds is not None:
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            south_west_bounds = bounds.get('_southWest')
            north_east_bounds = bounds.get('_northEast')

            if not (south_west_bounds.get('lat') <= latitude <= north_east_bounds.get('lat') and south_west_bounds.get('lng') <= longitude <= north_east_bounds.get('lng')):
                continue

        if zoom_level is not None:
            min_elevation = elevation_mapping.get(zoom_level)
            if min_elevation is not None and data.get('elevation') is not None and not min_elevation < data.get('elevation'):
                continue

        store.append(data)

    return store
