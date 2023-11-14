from django.shortcuts import render
from map.forms import SearchForm
from map.models import Search
from django_redis import get_redis_connection
from json import loads
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect


def get_zoom_level_bounds(request):
    data = loads(request.body.decode('utf-8'))
    zoom_level = data.get('zoom_level')
    bounds = data.get('bounds')

    return zoom_level, bounds


@csrf_protect
def process_request(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        zoom_level, bounds = get_zoom_level_bounds(request)
        marker_data = add_markers(filter=request.session.get('filter'), bounds=bounds, zoom_level=zoom_level)
        return JsonResponse({'status': 'success', 'markers': marker_data})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


@csrf_protect
def clear_filter(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        request.session.pop('filter', None)
        zoom_level, bounds = get_zoom_level_bounds(request)
        marker_data = add_markers(bounds=bounds, zoom_level=zoom_level)
        return JsonResponse({'status': 'success', 'markers': marker_data})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


def index(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            form.save()
            request.session['filter'] = Search.objects.last().location
            marker_data = add_markers(filter=request.session.get('filter'))
            return JsonResponse({'status': 'success', 'markers': marker_data})
    else:
        form = SearchForm()

    context = {'form': form, }
    return render(request, 'index.html', context)


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
