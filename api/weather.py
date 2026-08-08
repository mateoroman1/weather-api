from fastapi import APIRouter, Depends, HTTPException, status
from services.weather_service import WeatherService

router = APIRouter(prefix="/api")

@router.get("/weather/{location}")
def get_weather(location_name: str):
    # TODO: get db and pass to service constructor. That's DI, right?
    weather_service = WeatherService()
    data = weather_service.get_weather_by_location(location_name)

    return data