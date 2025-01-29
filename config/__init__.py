from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_PATH: str
    TRON_NETWORK: str
    TRON_TOKEN: str | None
    TRON_PROVIDER: str | None

    class Config:
        env_file = ".env"

settings = Settings() # noqa

