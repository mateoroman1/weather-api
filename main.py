from fastapi import FastAPI
from api import weather

app = FastAPI(title="Weather API")

app.include_router(weather.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
