from django.shortcuts import render
from map.forms import SearchForm
from django_redis import get_redis_connection
from json import loads
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect


def get_zoom_level_bounds_filter(request):
    data = loads(request.body.decode('UTF-8'))
    return data.get('form_data'), data.get('filter_value'), data.get('zoom_level'), data.get('bounds')


def get_filters_key(request):
    return f'user_filters:{request.user.id}'


def get_filter_list(request):
    redis = get_redis_connection()
    user_filters_key = get_filters_key(request)
    return [value.decode('utf-8') for value in redis.lrange(user_filters_key, 0, -1)]


def add_filter_to_redis(request, filter_value):
    redis = get_redis_connection()
    user_filters_key = get_filters_key(request)
    redis.rpush(user_filters_key, filter_value)


def remove_filter_from_redis(request, filter_value):
    redis = get_redis_connection()
    user_filters_key = get_filters_key(request)
    redis.lrem(user_filters_key, 0, filter_value)


def get_last_added_filter(request):
    redis = get_redis_connection()
    user_filters_key = get_filters_key(request)
    last_added_filter = redis.lindex(user_filters_key, -1).decode('utf-8')
    return last_added_filter


@csrf_protect
def process_request(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        _, _, zoom_level, bounds = get_zoom_level_bounds_filter(request)
        filter_list = get_filter_list(request)
        marker_data = add_markers(filter=filter_list, bounds=bounds, zoom_level=zoom_level)
        return JsonResponse({'status': 'success', 'markers': marker_data}, safe=False)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


def add_filter(request):
    if request.method == 'POST':
        _, filter_value, zoom_level, bounds = get_zoom_level_bounds_filter(request)
        add_filter_to_redis(request, filter_value=filter_value)
        filter_list = get_filter_list(request)
        marker_data = add_markers(filter=filter_list, bounds=bounds, zoom_level=zoom_level)
        last_added_filter = get_last_added_filter(request)

        return marker_data, last_added_filter


def remove_filter(request):
    if request.method == 'POST':
        _, filter_value, zoom_level, bounds = get_zoom_level_bounds_filter(request)
        remove_filter_from_redis(request, filter_value=filter_value)
        filter_list = get_filter_list(request)
        marker_data = add_markers(filter=filter_list, bounds=bounds, zoom_level=zoom_level)

        return JsonResponse({'status': 'success', 'markers': marker_data}, safe=False)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


def index(request):
    if request.method == 'POST':
        form_data, _, _, _ = get_zoom_level_bounds_filter(request)
        form = SearchForm(form_data)
        if form.is_valid():
            form.save()
            marker_data, last_added_filter = add_filter(request)
            return JsonResponse({'status': 'success', 'markers': marker_data, 'filters': last_added_filter}, safe=False)
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

        if filter is not None:
            flag = False
            for filter_value in filter:
                if filter_value not in data.values():
                    flag = True
                    break
            if flag:
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
