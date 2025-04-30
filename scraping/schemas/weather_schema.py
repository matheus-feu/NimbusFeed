from typing import Optional, Dict

from pydantic import BaseModel


class WeatherForecastSchema(BaseModel):
    city: Optional[str] = None
    temperature: Optional[Dict[str, str]] = None
    rain: Optional[str] = None
    wind: Optional[str] = None
    humidity: Optional[Dict[str, str]] = None
    sun: Optional[str] = None
    rainbow: Optional[str] = None