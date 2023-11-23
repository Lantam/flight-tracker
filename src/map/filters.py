from django_filters import FilterSet, NumberFilter

from map.models import Api


class ApiFilter(FilterSet):

    class Meta:
        model = Api
        fields = {
            'elevation': ['gte', 'lte', 'exact'],
        }
