from fastapi import APIRouter, Query
from fastapi import HTTPException, status

from scraping.rpa.base import CITY_IDS
from scraping.rpa.prevision import PrevisaoScraper
from scraping.schemas.weather_schema import WeatherForecastSchema

router = APIRouter()


@router.get("/previsao", response_model=WeatherForecastSchema)
async def get_weather_forecast(city_id: str = Query(..., description="ID da cidade"), ):
    """
    Rota para obter a previsão do tempo de uma cidade específica.

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
        scraper.close()
        return data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# @router.get("/cidades")
# async def get_cities_info():
#     data = {"cities": ["São Paulo", "Rio de Janeiro", "Curitiba"]}
#     return data


@router.get("/alertas")
async def get_weather_alerts(username: str = Query(...), password: str = Query(...)):
    scraper = ExtractClimateValues()
    scraper.login(username=username, password=password)
    data = {"alerts": ["Chuva forte em São Paulo"]}
    return data
