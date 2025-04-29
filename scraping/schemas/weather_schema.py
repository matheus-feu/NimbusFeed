from pydantic import BaseModel


class WeatherForecastSchema(BaseModel):
    city: str
    temperature: str
    rain: str
    wind: str
    humidity: str
    sun: str
