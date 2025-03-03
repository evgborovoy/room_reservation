from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str = "Бронирование переговорок"  # if 'app_title' not in configfile use default value
    database_url: str

    class Config:
        env_file = ".env"  # name of environment file


# create 1 time and use
settings = Settings()
