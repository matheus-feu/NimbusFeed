from sqlalchemy import Column, Integer, String, Float, JSON

from api.db.base_model import Base


class CityWeather(Base):
    __tablename__ = "city_weather"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, nullable=True)
    country = Column(String, nullable=True)
    temperature = Column(Float, nullable=True)
    feels_like = Column(Float, nullable=True)
    temp_min = Column(Float, nullable=True)
    temp_max = Column(Float, nullable=True)
    pressure = Column(Integer, nullable=True)
    humidity = Column(Integer, nullable=True)
    description = Column(String, nullable=True)
    wind_speed = Column(Float, nullable=True)
    wind_deg = Column(Integer, nullable=True)
    clouds = Column(Integer, nullable=True)
    sunrise = Column(String, nullable=True)
    sunset = Column(String, nullable=True)
    timezone = Column(String, nullable=True)


class WeatherForecast(Base):
    __tablename__ = "weather_forecast"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, nullable=True)
    temperature = Column(JSON, nullable=True)
    rain = Column(String, nullable=True)
    wind = Column(String, nullable=True)
    humidity = Column(JSON, nullable=True)
    sun = Column(String, nullable=True)
    rainbow = Column(String, nullable=True)
