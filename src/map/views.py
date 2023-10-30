from django.shortcuts import render
from folium import Icon, IFrame, Map, Marker, Popup
from map.forms import SearchForm
from map.models import Api, Search
from django_redis import get_redis_connection
from json import loads


m = Map(location=[0, 0], zoom_start=2, min_zoom=2, max_bounds=True)

redis = get_redis_connection()


def process_input(request, m, api_data, filter=None, form=None):
    if filter is not None:
        filtered_data = [data for data in (loads(value) for value in api_data.values()) if filter in data.values()]
        add_markers(m, filtered_data)
    else:
        decoded_data = [data for data in (loads(value) for value in api_data.values())]

        add_markers(m, decoded_data)

    represent_as_html = m._repr_html_()
    context = {'m': represent_as_html, }
    if form is not None:
        context['form'] = form
    return render(request, 'index.html', context)


def index(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            form.save()
            filter = Search.objects.last().location
            return process_input(request, m, redis.hgetall("cache"), filter, form)
    else:
        form = SearchForm()

    represent_as_html = m._repr_html_()
    context = {'m': represent_as_html, 'form': form, }
    return render(request, 'index.html', context)


def add_all_markers(request):
    return process_input(request, m, redis.hgetall("cache"))


def add_markers(m, api_data):
    for i in api_data:
        values = list(i.values())
        html = f'''
            Registration Number: {values[0]}<br>
            Country Code: {values[1]}<br>
            Longitude: {values[2]}<br>
            Latitude: {values[3]}<br>
            Elevation: {values[4]}<br>
            Head Direction: {values[5]}<br>
            Airline ICAO: {values[6]}<br>
            Aircraft ICAO: {values[7]}<br>
            Departure ICAO: {values[8]}<br>
            Arrival ICAO: {values[9]}<br>
            Status: {values[10]}<br>
        '''
        iframe = IFrame(html, width=200, height=200)
        popup = Popup(iframe, max_width=200)

        Marker(
            [values[2], values[3]],
            tooltip='Click for more',
            popup=popup,
            icon=Icon(icon='plane', angle=90),
        ).add_to(m)
