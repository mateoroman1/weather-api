from fastapi import FastAPI
from api import weather

# api request -> weather service -> weather client session makes openmeteo request -> geocode -> get weather data -> repository -> db

app = FastAPI(title="Weather API")

app.include_router(weather.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
