from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from flight_tracker.settings import AIRLABS_API_KEY
from folium import Icon, IFrame, Map, Marker, Popup
from .forms import SearchForm
from .models import Api, Search
from requests import get

def add_latest_api_data(request=None):
    api_key = AIRLABS_API_KEY
    url = f'https://airlabs.co/api/v9/flights?_view=array&_fields=flag,lat,lng,alt,dir,airline_icao,aircraft_icao,dep_icao,arr_icao,status&api_key={api_key}'
    response = get(url).json()
    Api.objects.create(response=response)

    if request is not None:
        return render(request, 'index.html')

def get_response():
    try:
        return Api.objects.latest('response').response
    except ObjectDoesNotExist:
        add_latest_api_data()
        return Api.objects.latest('response').response

def filter_input(m, api_data):
    try:
        filter = Search.objects.last().location
        add_markers(m, api_data, filter=filter)
    except ObjectDoesNotExist:
        pass

def index(request):
    m = Map(location=[0, 0], zoom_start=2, min_zoom=2, max_bounds=True)
    api_data = get_response()

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            form.save()
            filter_input(m, api_data)
            m = m._repr_html_()
            context = {
                'm': m,
                'form': form,
            }
            return render(request, 'index.html', context)
    else:
        form = SearchForm()
    
    m = m._repr_html_()
    context = {
        'm': m,
        'form': form,
    }
    return render(request, 'index.html', context)


def add_all_markers(request):
    api_data = get_response()

    m = Map(location=[0, 0], zoom_start=2, max_bounds=True)
    add_markers(m, api_data)

    m = m._repr_html_()
    context = {
        'm': m,
    }
    return render(request, 'index.html', context)

def add_markers(m, api_data, filter=None):
    for i in api_data:
        html = f'''
            Country Code: {i[0]}<br>
            Longitude: {i[1]}<br>
            Latitude: {i[2]}<br>
            Elevation: {i[3]}<br>
            Head Direction: {i[4]}<br>
            Airline ICAO: {i[5]}<br>
            Aircraft ICAO: {i[6]}<br>
            Departure ICAO: {i[7]}<br>
            Arrival ICAO: {i[8]}<br>
            Status: {i[9]}<br>
        '''
        iframe = IFrame(html, width=200, height=200)
        popup = Popup(iframe, max_width=200)

        if filter is not None:
            for j in i:
                if str(j) == str(filter):
                    Marker(
                        [i[1], i[2]],
                        tooltip='Click for more',
                        popup=popup,
                        icon=Icon(icon='plane', angle=90)
                    ).add_to(m)
        else:
            Marker(
                [i[1], i[2]],
                tooltip='Click for more',
                popup=popup,
                icon=Icon(icon='plane', angle=90)
            ).add_to(m)
