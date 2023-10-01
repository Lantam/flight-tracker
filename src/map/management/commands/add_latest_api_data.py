from typing import Any
from django.core.management.base import BaseCommand

from map.models import Api
from map.utils import AirlabsSDK


class Command(BaseCommand):

    def handle(self, *args, **options) -> None:
        sdk = AirlabsSDK()
        fields = [
            'flag',
            'lat',
            'lng',
            'alt',
            'dir',
            'airline_icao',
            'aircraft_icao',
            'dep_icao',
            'arr_icao',
            'status',
        ]

        response_raw = sdk.get_latest_api_data(fields=fields)
        response = response_raw.get('response')

        if response is not None:
            for response_item in response:
                Api.objects.update_or_create(
                    registration_number=response_item.get('reg_number'),
                    defaults={
                        'country_code': response_item.get('flag'),
                        'latitude': response_item.get('lat'),
                        'longitude': response_item.get('lng'),
                        'elevation': response_item.get('alt'),
                        'head_direction': response_item.get('dir'),
                        'airline_icao': response_item.get('airline_icao'),
                        'aircraft_icao': response_item.get('aircraft_icao'),
                        'departure_icao': response_item.get('dep_icao'),
                        'arrival_icao': response_item.get('arr_icao'),
                        'status': response_item.get('status')
                    }
                )
