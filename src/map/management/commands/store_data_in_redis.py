from django.core.management.base import BaseCommand
from map.models import Api
from django_redis import get_redis_connection
from json import dumps


class Command(BaseCommand):

    def handle(self, *args, **options) -> None:
        redis = get_redis_connection()
        api_data = Api.objects.filter(status='en-route')

        for data in api_data:
            data_dict = {
                'registration_number': data.registration_number,
                'country_code': data.country_code,
                'latitude': data.latitude,
                'longitude': data.longitude,
                'elevation': data.elevation,
                'head_direction': data.head_direction,
                'airline_icao': data.airline_icao,
                'aircraft_icao': data.aircraft_icao,
                'departure_icao': data.departure_icao,
                'arrival_icao': data.arrival_icao,
                'status': data.status,
            }

            json_data = dumps(data_dict)

            redis_key = f'api_data:{data.id}'
            redis.hset("cache", redis_key, json_data)
