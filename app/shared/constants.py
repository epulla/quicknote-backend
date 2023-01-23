from ..config import get_settings
import os

settings = get_settings()

REDIS_HOST = settings.redis_host
REDIS_PORT = settings.redis_port
REDIS_PASSWORD = settings.redis_password
REDIS_SSL = settings.redis_ssl
URL_SEPARATOR = settings.url_separator # Default: "&&&"
USE_URL_SHORTER = settings.use_url_shorter # Default: True
MAX_LENGTH_NOTE_CONTENT = settings.max_length_note_content # Default: 3000 (same as frontend)
