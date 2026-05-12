from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://bracelet:bracelet@localhost:5432/bracelet"

    model_config = {"env_prefix": "BRACELET_", "env_file": ".env", "extra": "ignore"}


settings = Settings()
