import os
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    redis_host: str = os.getenv("REDIS_HOST", "localhost")
    redis_port: int = os.getenv("REDIS_PORT", 6379)
    redis_password: str = os.getenv("REDIS_PASSWORD", "")
    redis_ssl: bool = (os.getenv("REDIS_SSL", "true").lower() == "true")
    url_separator: str = os.getenv("URL_SEPARATOR", "&&&")
    use_url_shorter: bool = (os.getenv("USE_URL_SHORTER", "true").lower() == "true")
    max_length_note_content: int = os.getenv("MAX_LENGTH_NOTE_CONTENT", 3000)

    class Config:
      env_file = ".env"


@lru_cache
def get_settings():
    return Settings()
