from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_PATH: str
    TRON_NETWORK: str
    TRON_TOKEN: str | None
    TRON_PROVIDER: str | None
    model_config = ConfigDict(env_file = ".env") # noqa

settings = Settings() # noqa

