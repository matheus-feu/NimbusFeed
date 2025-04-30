from decouple import config


class Settings:
    API_KEY: str = config("API_KEY")
    HOST: str = config("HOST")
    PORT: int = config("PORT", cast=int)
    NAME_APP: str = config("NAME_APP")
    DATABASE_URL: str = config("DATABASE_URL")
    USE_HEADLESS: bool = config("USE_HEADLESS", cast=bool, default=True)
    USE_SELENOID: bool = config("USE_SELENOID", cast=bool, default=True)


settings: Settings() = Settings()
