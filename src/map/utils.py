from requests import get

from flight_tracker.settings import AIRLABS_API_KEY, AIRLABS_BASE_URL
from map.models import Api


class AirlabsSDK:

    def get_latest_api_data(self, fields: list = []) -> dict:
        api_key = AIRLABS_API_KEY
        field_names = ''.join(fields)
        url = f'{AIRLABS_BASE_URL}?_fields={field_names}&api_key={api_key}'
        response = get(url)
        return response.json()
