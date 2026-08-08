from pydantic import BaseModel, ConfigDict, Json, Field
from typing import Any
from datetime import datetime

class AppModel(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

class WeatherBase(AppModel):
    id: Any | None = None
    success: bool
    requested_location: str
    resolved_location: str
    latitude: float
    longitude: float
    timestamp: datetime = Field(default_factory=datetime.now)

# Persistence object
# Seems like from the requirements we're wanting to
# store requests to the external api.
class RequestRecord(BaseModel):
    id: Any | None = None
    response: int | None = None # Not sure why these are coming up null # Forgot the response in the INSERT lmao
    timestamp: datetime = Field(default_factory=datetime.now)
    requested_location: str
    resolved_location: str
    latitude: float
    longitude: float
    data: Any | None = None