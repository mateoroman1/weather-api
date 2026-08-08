import openmeteo_requests
import httpx

import requests_cache
from retry_requests import retry

GEOCODE_BASE_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_BASE_URL = "https://api.open-meteo.com/v1/forecast"

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

    def get_weather_data(self, latitude, longitude):

        # Not customizing any of the params yet, just getting basic weather info
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "is_day", "precipitation", "cloud_cover", "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m"]
        }
        responses = openmeteo.weather_api(WEATHER_BASE_URL, params = params)

        response = responses[0]

        current = response.Current()

        # indexing of current variables is identical to params
        weather_data = {
            "latitude": response.Latitude(),
            "longitude": response.Longitude(),
            "temperature": current.Variables(0).Value(),
            "humidity": current.Variables(1).Value(),
            "feels_like": current.Variables(2).Value(),
            "is_day": current.Variables(3).Value(),
            "precipitation": current.Variables(4).Value(),
            "cloud_cover": current.Variables(5).Value(),
            "wind_speed": current.Variables(6).Value(),
            "wind_direction": current.Variables(7).Value(),
            "wind_gusts": current.Variables(8).Value()
        }

        return weather_data