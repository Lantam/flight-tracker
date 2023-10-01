from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from folium import Icon, IFrame, Map, Marker, Popup
from .forms import SearchForm
from .models import Api, Search



api_data = [
    [
        row.registration_number,
        row.country_code,
        row.latitude,
        row.longitude,
        row.elevation,
        row.head_direction,
        row.airline_icao,
        row.aircraft_icao,
        row.departure_icao,
        row.arrival_icao,
        row.status,
    ]
    for row in Api.objects.all()
]


def filter_input(m, api_data):
    try:
        filter = Search.objects.last().location
        add_markers(m, api_data, filter=filter)
    except ObjectDoesNotExist:
        pass

def index(request):
    m = Map(location=[0, 0], zoom_start=2, min_zoom=2, max_bounds=True)

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

    m = Map(location=[0, 0], zoom_start=2, min_zoom=2, max_bounds=True)
    add_markers(m, api_data)

    m = m._repr_html_()
    context = {
        'm': m,
    }
    return render(request, 'index.html', context)

def add_markers(m, api_data, filter=None):
    for i in api_data:
        html = f'''
            Registration Number: {i[0]}<br>
            Country Code: {i[1]}<br>
            Longitude: {i[2]}<br>
            Latitude: {i[3]}<br>
            Elevation: {i[4]}<br>
            Head Direction: {i[5]}<br>
            Airline ICAO: {i[6]}<br>
            Aircraft ICAO: {i[7]}<br>
            Departure ICAO: {i[8]}<br>
            Arrival ICAO: {i[9]}<br>
            Status: {i[10]}<br>
        '''
        iframe = IFrame(html, width=200, height=200)
        popup = Popup(iframe, max_width=200)

        if filter is not None:
            for j in i:
                if str(j) == str(filter):
                    Marker(
                        [i[2], i[3]],
                        tooltip='Click for more',
                        popup=popup,
                        icon=Icon(icon='plane', angle=90),
                    ).add_to(m)
        else:
            Marker(
                [i[2], i[3]],
                tooltip='Click for more',
                popup=popup,
                icon=Icon(icon='plane', angle=90),
            ).add_to(m)
