from pydantic import BaseModel, ConfigDict
from typing import Any
from datetime import date

class AppModel(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

class WeatherBase(AppModel):
    id: Any | None = None
    success: bool
    requested_location: str
    resolved_location: str
    latitude: float
    longitude: float
    timestamp: date

class WeatherResult(WeatherBase):
    data: Any | None = None

# Persistence object
# Seems like from the requirements we're wanting to
# store requests to the external api.
class RequestRecord(BaseModel):
    id: Any | None = None
    response: int
    timestamp: date
    requested_location: str
    resolved_location: str
    latitude: float
    longitude: float
    data: Any | None = None