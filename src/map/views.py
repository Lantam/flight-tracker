from django.shortcuts import render
from folium import Icon, IFrame, Map, Marker, Popup
from map.forms import SearchForm
from map.models import Search
from django_redis import get_redis_connection
from json import loads


m = Map(location=[0, 0], zoom_start=2, min_zoom=2, max_bounds=True)


def index(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            form.save()
            filter = Search.objects.last().location
            add_markers(m, filter)
    else:
        form = SearchForm()

    represent_as_html = m._repr_html_()
    context = {'m': represent_as_html, 'form': form, }
    return render(request, 'index.html', context)


def add_all_markers(request):
    add_markers(m)

    represent_as_html = m._repr_html_()
    context = {'m': represent_as_html}
    return render(request, 'index.html', context)


def add_markers(m, filter=None):
    redis = get_redis_connection()
    api_data = redis.hgetall("cache")

    for value in api_data.values():
        data = loads(value)

        if filter is not None and filter not in data.values():
            continue

        html = f'''
            Registration Number: {data.get('registration_number')}<br>
            Country Code: {data.get('country_code')}<br>
            Longitude: {data.get('longitude')}<br>
            Latitude: {data.get('latitude')}<br>
            Elevation: {data.get('elevation')}<br>
            Head Direction: {data.get('head_direction')}<br>
            Airline ICAO: {data.get('airline_icao')}<br>
            Aircraft ICAO: {data.get('aircraft_icao')}<br>
            Departure ICAO: {data.get('departure_icao')}<br>
            Arrival ICAO: {data.get('arrival_icao')}<br>
            Status: {data.get('status')}<br>
        '''
        iframe = IFrame(html, width=200, height=200)
        popup = Popup(iframe, max_width=200, lazy=True)

        Marker(
            [data.get('latitude'), data.get('longitude')],
            tooltip='Click for more',
            popup=popup,
            icon=Icon(icon='plane', angle=90),
        ).add_to(m)
