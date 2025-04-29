from scraping.rpa.base import BaseScraper
from scraping.schemas.weather_schema import WeatherForecastSchema


class PrevisaoScraper(BaseScraper):
    def __init__(self, id_city: str, city: str):
        url = f"https://www.climatempo.com.br/previsao-do-tempo/cidade/{id_city}/{city}"
        super().__init__(url)

    def __enter__(self):
        return self

    def extract_data(self):
        self.wait_loads()

        city = self.wait_xpath("//h1[@class='-bold -font-18 _margin-b-5']").text
        temperature = self.wait_xpath("//p[@class='-gray -line-height-24 _center']").text
        rain = self.wait_xpath("//span[contains(text(), 'Chuva')]/following-sibling::span").text
        wind = self.wait_xpath("//span[contains(text(), 'Vento')]/following-sibling::span").text
        humidity = self.wait_xpath("//span[contains(text(), 'Umidade')]/following-sibling::span").text
        sun = self.wait_xpath("//span[contains(text(), 'Sol')]/following-sibling::span").text

        return WeatherForecastSchema(
            city=city,
            temperature=temperature,
            rain=rain,
            wind=wind,
            humidity=humidity,
            sun=sun
        )
