from pydantic_settings import BaseSettings, SettingsConfigDict # type: ignore
from pydantic import Field # type: ignore

class Settings(BaseSettings):
    app_name: str = "task-api"
    # Default to SQLite for dev; tests will override with PostgreSQL URL
    database_url: str = Field(default="sqlite:///./dev.db", alias="DATABASE_URL")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
