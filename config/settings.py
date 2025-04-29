from decouple import config


class Settings:
    API_KEY: str = config("API_KEY")
    CITY: str = config("CITY")
    LINK_TEMPLATE: str = config("LINK")
    HOST: str = config("HOST")
    PORT: int = config("PORT", cast=int)
    NAME: str = config("NAME")

    @property
    def formatted_link(self) -> str:
        return self.LINK_TEMPLATE.format(CITY=self.CITY, API_KEY=self.API_KEY)


settings: Settings() = Settings()