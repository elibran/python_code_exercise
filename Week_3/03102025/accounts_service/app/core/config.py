from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict # type: ignore
from pydantic import Field # type: ignore
import os
from dotenv import load_dotenv # type: ignore

# --- Auto-select .env by APP_ENV ---
_env_raw = os.getenv("APP_ENV", "development").lower()
if _env_raw.startswith("prod"):
    _env_file = ".env.prod"
else:
    _env_file = ".env.dev"
load_dotenv(_env_file)

class AppSettings(BaseSettings):
    app_env: str = Field("development", alias="APP_ENV")
    database_url: str = Field("sqlite:///./data/dev.db", alias="DATABASE_URL")
    log_level: str = Field("INFO", alias="LOG_LEVEL")
    email_outbox_file: str = Field("./data/dev_emails.log", alias="EMAIL_OUTBOX_FILE")

    model_config = SettingsConfigDict(env_file=_env_file, env_file_encoding="utf-8", extra="ignore")

@lru_cache(maxsize=1)
def get_settings() -> AppSettings:
    return AppSettings()
