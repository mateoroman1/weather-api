import logging

from client.weather_client import WeatherClient
from models.schemas import RequestRecord
from models.database import WeatherRepository

logger = logging.getLogger(__name__)

class WeatherService:

    def __init__(self):
        self.weather_client = WeatherClient()
        self.weather_repository = WeatherRepository()

    def get_weather_by_location(self, location_name: str):
        logger.info(f"Geocoding location {location_name}")

        # request geocode from weather client
        geocode_result = self.weather_client.get_geocode_match(location_name)

        #TODO: validate response

        # request weather data
        weather_data = self.weather_client.get_weather_data(geocode_result)

        #TODO: validate response
        record = RequestRecord(
            id=geocode_result.id,
            response=200,
            requested_location=geocode_result.requested_location,
            resolved_location=geocode_result.resolved_location,
            latitude=geocode_result.latitude,
            longitude=geocode_result.longitude,
            data=weather_data
        )

        WeatherRepository.save_request(record)


        return weather_data

    def get_request_history(self):
        requests = WeatherRepository.get_request_history()

        return requests

