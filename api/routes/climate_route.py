from fastapi import APIRouter, Query
from fastapi import Depends
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from api.db.session import get_db
from api.models.weather import WeatherForecast, CityWeather
from api.schemas.weather_schema import WeatherSchema
from api.services.openweather_service import OpenWeatherService
from scraping.rpa.base import CITY_IDS
from scraping.rpa.prevision import PrevisaoScraper
from scraping.schemas.weather_schema import WeatherForecastSchema

router = APIRouter()


@router.get("/forecast", response_model=WeatherForecastSchema)
async def get_weather_forecast(
        city_id: str = Query(..., description="ID da cidade"),
        db: Session = Depends(get_db)
):
    """
    Rota para obter a previsão do tempo de uma cidade específica. Essa rota realiza o scraping no site
    ClimaTempo e retorna os dados climáticos em JSON.

    :param city_id: ID da cidade para a qual deseja obter a previsão do tempo.
    IDs permitidos:
    **558** (São Paulo),
    **321** (Rio de Janeiro),
    **61** (Brasília).

    :return: Dados da previsão do tempo.
    """
    city_data = next((data for data in CITY_IDS.values() if data.get("id") == city_id), None)
    if not city_data or not city_data.get("id") or not city_data.get("url_name"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cidade não encontrada ou dados incompletos no mapeamento"
        )

    try:
        scraper = PrevisaoScraper(id_city=city_data["id"], city=city_data["url_name"])
        data = scraper.extract_data()
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Previsão do tempo não encontrada"
            )
        scraper.close()

        forecast_data = WeatherForecast(
            city=data.city,
            temperature=data.temperature,
            rain=data.rain,
            wind=data.wind,
            humidity=data.humidity,
            sun=data.sun,
            rainbow=data.rainbow,
        )
        db.add(forecast_data)
        db.commit()
        db.refresh(forecast_data)

        return data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/city", response_model=WeatherSchema)
async def get_city_info(
        city_name: str = Query(..., description="Nome da cidade"),
        db: Session = Depends(get_db)
):
    """
    Rota para obter informações climáticas de uma cidade específica. Embora essa rota utilize a API OpenWeather,
    ela não realiza scraping. Em vez disso, ela faz uma chamada à API para obter dados climáticos.

    :param city_name: Nome da cidade para a qual deseja obter informações.
    :return: Informações sobre a cidade.
    """
    data = OpenWeatherService.get_weather_data(city_name)
    if not data:
        raise HTTPException(status_code=404, detail="Cidade não encontrada ou erro ao acessar a API")

    weather_data = WeatherSchema.from_api_response(data)

    city_weather = CityWeather(
        city=weather_data.city,
        country=weather_data.country,
        temperature=weather_data.temperature,
        feels_like=weather_data.feels_like,
        temp_min=weather_data.temp_min,
        temp_max=weather_data.temp_max,
        pressure=weather_data.pressure,
        humidity=weather_data.humidity,
        description=weather_data.description,
        wind_speed=weather_data.wind_speed,
        wind_deg=weather_data.wind_deg,
        clouds=weather_data.clouds,
        sunrise=weather_data.sunrise,
        sunset=weather_data.sunset,
        timezone=weather_data.timezone,
    )
    db.add(city_weather)
    db.commit()
    db.refresh(city_weather)

    return weather_data
