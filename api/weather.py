from fastapi import APIRouter, Depends, HTTPException, status
from services.weather_service import WeatherService
from models.schemas import RequestRecord

router = APIRouter(prefix="/api")

@router.get("/weather/{location}")
def get_weather(location: str):
    weather_service = WeatherService()
    data = weather_service.get_weather_by_location(location)

    return data

@router.get("/requests")
def get_history():
    weather_service = WeatherService()
    data = weather_service.get_request_history()

    return data