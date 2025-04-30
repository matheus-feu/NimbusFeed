from requests.exceptions import RequestException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from tenacity import *

from api.logger import app_logger
from scraping.rpa.base import BaseScraper
from scraping.schemas.weather_schema import WeatherForecastSchema


class PrevisaoScraper(BaseScraper):
    def __init__(self, id_city: str, city: str):
        url = f"https://www.climatempo.com.br/previsao-do-tempo/cidade/{id_city}/{city}"
        super().__init__(url)

    def __enter__(self):
        return self

    def extract_sun_data(self, sun) -> str:
        """
        Extracts the sunrise and sunset times from the sun element.
        :param sun:
        :return:
        """
        sunrise = sun.find_element(By.XPATH, ".//span[1]").text.strip()
        sunset = sun.find_element(By.XPATH, ".//span[last()]").text.strip()
        return f"{sunrise} - {sunset}"

    def extract_temperature_data(self, temperature) -> dict:
        """
        Extracts the minimum and maximum temperature from the temperature element.
        :param temperature:
        :return:
        """
        temp_text = temperature.find_element(By.CLASS_NAME, "_flex").text.strip()
        temp_min, temp_max = temp_text.split("\n")
        return {"min": temp_min.strip(), "max": temp_max.strip()}

    def extract_humidity_data(self, humidity) -> dict:
        """
        Extracts the minimum and maximum humidity from the humidity element.
        :param humidity:
        :return:
        """
        humidity_text = humidity.find_element(By.CLASS_NAME, "_flex").text.strip()
        min_humidity, max_humidity = humidity_text.split("\n")
        return {"min": min_humidity.strip(), "max": max_humidity.strip()}

    def extract_rainbow_data(self, rainbow):
        return rainbow.find_element(By.CLASS_NAME, "-gray-light").text.strip()

    def extract_default_data(self, default):
        return default.find_element(By.CLASS_NAME, "_flex").text.strip()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(2),
        retry=retry_if_exception_type((WebDriverException, RequestException, Exception))
    )
    def extract_data(self):
        """
        Extracts weather data from the page.

        3 attempts to load the page and extract data.
        Wait for 2 seconds between attempts.
        Retry if an exception occurs.

        :return: WeatherForecastSchema object with the extracted data.
        """
        self.wait_loads()

        try:
            self.driver.find_element(
                By.XPATH,
                '//button[contains(@class, "cookie-consent-btn") and text()="OK"]'
            ).click()

            prevision_city = self.wait_xpath(
                "//h1[contains(@class, '-bold -font-18') and contains(@class, '-dark-blue')]"
            ).text

            variables_list = self.driver.find_element(By.CLASS_NAME, "variables-list")
            variables = variables_list.find_elements(By.TAG_NAME, "li")

            data = {}

            key_to_method = {
                "Sol": self.extract_sun_data,
                "Temperatura": self.extract_temperature_data,
                "Umidade": self.extract_humidity_data,
                "Previsão de arco-íris": self.extract_rainbow_data,
            }
            for variable in variables:
                try:
                    key = variable.find_element(By.CLASS_NAME, "variable").text.strip()
                    method = key_to_method.get(key, self.extract_default_data)
                    value = method(variable)
                    data[key] = value
                except Exception as e:
                    app_logger.error(f"Erro ao extrair dados da variável: {key}. Erro: {e}")
                    continue

            return WeatherForecastSchema(
                city=prevision_city,
                temperature=data.get("Temperatura"),
                rain=data.get("Chuva"),
                wind=data.get("Vento"),
                humidity=data.get("Umidade"),
                sun=data.get("Sol"),
                rainbow=data.get("Previsão de arco-íris")
            )
        except Exception as e:
            app_logger.error(f"Erro ao extrair dados: {e}")
            return None
