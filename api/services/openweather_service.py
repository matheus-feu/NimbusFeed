from typing import Optional

import requests

from config.settings import settings


class OpenWeatherService:
    LINK_TEMPLATE = "https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&lang=pt_br"

    @classmethod
    def get_weather_data(cls, city_name: str) -> Optional[dict]:
        """
        Faz a requisição à API do OpenWeather para obter os dados climáticos de uma cidade.
        :param city_name: Nome da cidade.
        :return: Dados brutos da API ou None em caso de erro.
        """
        link = cls.LINK_TEMPLATE.format(CITY=city_name, API_KEY=settings.API_KEY)

        try:
            response = requests.get(link)
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            return None
