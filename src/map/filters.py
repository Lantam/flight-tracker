from django_filters import FilterSet, CharFilter
from django.db.models import Q

from map.models import Api


class ApiFilter(FilterSet):
    search = CharFilter(method='filter_search')

    class Meta:
        model = Api
        fields = {
            'elevation': ['gte', 'lte', 'exact'],
            'latitude': ['gte', 'lte', 'exact'],
            'longitude': ['gte', 'lte', 'exact'],
        }

    def filter_search(self, queryset, name, value):
        if value.isdigit():
            return self.filter_digit_fields(queryset, value)
        elif isinstance(value, str):
            return self.filter_string_fields(queryset, value)

    def filter_digit_fields(self, queryset, value):
        return queryset.filter(
            Q(latitude__icontains=value)
            | Q(longitude__icontains=value)
            | Q(elevation=value)
            | Q(head_direction=value)
        )

    def filter_string_fields(self, queryset, value):
        return queryset.filter(
            Q(registration_number=value)
            | Q(country_code=value)
            | Q(airline_icao=value)
            | Q(aircraft_icao=value)
            | Q(departure_icao=value)
            | Q(arrival_icao=value)
            | Q(status=value)
        )
