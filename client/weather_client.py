import openmeteo_requests
import httpx

import requests_cache
from retry_requests import retry

GEOCODE_BASE_URL = "https://geocoding-api.open-meteo.com/v1/search"

# Setup the Open-Meteo API client with cache and retry on error
# TODO: would be wise to variablize these at some point
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

class WeatherClient():
    def __init__(self):

        self.client = httpx.Client()

    def get_geocode_match(self, location: str):

        url = f"{GEOCODE_BASE_URL}?name={location}&count=1"

        response = self.client.get(url=url)

        payload = response.json()

        resolved_location = payload["results"][0]

        return {
            "requested_location": location,
            "resolved_location": resolved_location.get('name', ""),
            "latitude": resolved_location.get('latitude', 0),
            "longitude": resolved_location.get('longitude')
            }