import csv
from io import StringIO

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from api.db.session import get_db
from api.models.weather import CityWeather, WeatherForecast

router = APIRouter()


@router.get("/report/city_weather/csv")
def generate_city_weather_csv_report(db: Session = Depends(get_db)):
    """
    Gera um relatório CSV com os dados de CityWeather salvos no banco de dados.
    Esse relatório são os dados climáticos obtidos da API OpenWeatherMap.
    Sendo possível primeiro obter os dados no endpoint /api/city e depois baixar o relatório.
    """
    weather_data = db.query(CityWeather).all()

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Cidade",
        "País",
        "Temperatura",
        "Sensação Térmica",
        "Temp. Mínima",
        "Temp. Máxima",
        "Pressão",
        "Umidade",
        "Descrição",
        "Velocidade do Vento",
        "Direção do Vento",
        "Nuvens",
        "Nascer do Sol",
        "Pôr do Sol",
        "Fuso Horário"
    ])
    for weather in weather_data:
        writer.writerow([
            weather.city,
            weather.country,
            weather.temperature,
            weather.feels_like,
            weather.temp_min,
            weather.temp_max,
            weather.pressure,
            weather.humidity,
            weather.description,
            weather.wind_speed,
            weather.wind_deg,
            weather.clouds,
            weather.sunrise,
            weather.sunset,
            weather.timezone,
        ])

    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=city_weather_report.csv"}
    )


@router.get("/report/weather_forecast/csv")
def generate_weather_forecast_csv_report(db: Session = Depends(get_db)):
    """
    Gera um relatório CSV com os dados de WeatherForecast salvos no banco de dados.
    Esse relatório são os dados climáticos obtidos apartir do scraping do site Climatempo.
    Sendo possível primeiro obter os dados no endpoint /api/forecast e depois baixar o relatório.
    """
    forecast_data = db.query(WeatherForecast).all()

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Cidade",
        "Temperatura",
        "Chuva",
        "Vento",
        "Umidade",
        "Sol",
        "Arco-Íris"
    ])
    for forecast in forecast_data:
        writer.writerow([
            forecast.city,
            forecast.temperature,
            forecast.rain,
            forecast.wind,
            forecast.humidity,
            forecast.sun,
            forecast.rainbow
        ])

    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=weather_forecast_report.csv"}
    )
