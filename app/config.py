import os
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    url_separator: str = os.getenv("URL_SEPARATOR", "&&&")
    use_url_shorter: bool = (os.getenv("USE_URL_SHORTER", "True") == "True")
    max_length_note_content: int = os.getenv("MAX_LENGTH_NOTE_CONTENT", 3000)


@lru_cache
def get_settings():
    return Settings()
