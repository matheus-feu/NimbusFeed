from config.settings import settings
from libs.selenium import SetupDriver


CITY_IDS = {
    "sao_paulo": {"id": "558", "url_name": "saopaulo-sp"},
    "rio_de_janeiro": {"id": "321", "url_name": "riodejaneiro-rj"},
    "brasilia": {"id": "61", "url_name": "brasilia-df"},
}


class BaseScraper(SetupDriver):
    """
    Classe BaseScraper para configuração do Selenium WebDriver.
    Esta classe herda de SetupDriver e é responsável por inicializar o driver
    """

    def __init__(self, url: str):
        super().__init__(url=url, selenoid=True, headless=False)
        self.driver = super().setup(host=settings.HOST, name=settings.NAME)
        self.start_driver()

    def close(self):
        """
        Fecha o driver do Selenium.
        """
        self.driver.quit()



