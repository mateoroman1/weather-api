import logging
from client import weather_client

logger = logging.getLogger(__name__)

class WeatherService:

    def __init__(self):
        self.weather_client = weather_client.WeatherClient()

    def get_weather_by_location(self, location_name: str):
        logger.info(f"Geocoding location {location_name}")

        # request geocode from weather client
        geocode_result = self.weather_client.get_geocode_match(location_name)

        # validate response

        # request weather data

        # validate response

        # return
        return geocode_result
