from datetime import datetime, timezone, timedelta
from typing import Optional

from pydantic import BaseModel


class WeatherSchema(BaseModel):
    """
    Torna-se um modelo de dados para armazenar informações climáticas de uma cidade.
    A classe é justamene para definir o modelo de dados e conter apenas informações
    mais relevantes comparadas ao retorno vindo do Scraping do site Climatempo.
    """
    city: Optional[str] = None
    country: Optional[str] = None
    temperature: Optional[float] = None
    feels_like: Optional[float] = None
    temp_min: Optional[float] = None
    temp_max: Optional[float] = None
    pressure: Optional[int] = None
    humidity: Optional[int] = None
    description: Optional[str] = None
    wind_speed: Optional[float] = None
    wind_deg: Optional[int] = None
    clouds: Optional[int] = None
    sunrise: Optional[str] = None
    sunset: Optional[str] = None
    timezone: Optional[str] = None

    @classmethod
    def from_api_response(cls, data: dict) -> "WeatherSchema":
        def kelvin_to_celsius(kelvin: float) -> float:
            """
            Converte a temperatura de Kelvin para Celsius.

            """
            return round(kelvin - 273.15, 2)

        def format_time(timestamp: int, tz_offset: int) -> str:
            """
            Formata o timestamp em um horário legível.
            """
            tz = timezone(timedelta(seconds=tz_offset))
            return datetime.fromtimestamp(timestamp, tz).strftime("%H:%M:%S")

        def format_timezone(offset: int) -> str:
            """
            Formata o offset de timezone em uma string legível.
            Horário UTC com o formato UTC±HH:MM.
            """
            hours = offset // 3600
            minutes = abs(offset) % 3600 // 60
            return f"UTC{'+' if hours >= 0 else '-'}{abs(hours):02}:{minutes:02}"

        """
        Retorno completo da API OpenWeatherMap.
        
        {
           "base":"stations",
           "clouds":{
              "all":75
           },
           "cod":200,
           "coord":{
              "lat":-22.9028,
              "lon":-43.2075
           },
           "dt":1745982659,
           "id":3451190,
           "main":{
              "feels_like":295.48,
              "grnd_level":1017,
              "humidity":88,
              "pressure":1015,
              "sea_level":1015,
              "temp":294.95,
              "temp_max":295.13,
              "temp_min":294.15
           },
           "name":"Rio de Janeiro",
           "sys":{
              "country":"BR",
              "id":2098643,
              "sunrise":1746004315,
              "sunset":1746044875,
              "type":2
           },
           "timezone":-10800,
           "visibility":10000,
           "weather":[
              {
                 "description":"nublado",
                 "icon":"04n",
                 "id":803,
                 "main":"Clouds"
              }
           ],
           "wind":{
              "deg":10,
              "speed":2.06
           }
        }
        """

        return cls(
            city=data.get("name"),
            country=data["sys"].get("country"),
            temperature=kelvin_to_celsius(data["main"].get("temp", 0.0)),
            feels_like=kelvin_to_celsius(data["main"].get("feels_like", 0.0)),
            temp_min=kelvin_to_celsius(data["main"].get("temp_min", 0.0)),
            temp_max=kelvin_to_celsius(data["main"].get("temp_max", 0.0)),
            pressure=data["main"].get("pressure"),
            humidity=data["main"].get("humidity"),
            description=data["weather"][0].get("description"),
            wind_speed=data["wind"].get("speed"),
            wind_deg=data["wind"].get("deg"),
            clouds=data["clouds"].get("all"),
            sunrise=format_time(data["sys"].get("sunrise"), data.get("timezone")),
            sunset=format_time(data["sys"].get("sunset"), data.get("timezone")),
            timezone=format_timezone(data.get("timezone")),
        )