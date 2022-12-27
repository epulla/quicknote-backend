from ..config import get_settings

settings = get_settings()

REDIS_URL = settings.redis_url # Default: "redis://localhost:6379"
URL_SEPARATOR = settings.url_separator # Default: "&&&"
USE_URL_SHORTER = settings.use_url_shorter # Default: True
MAX_LENGTH_NOTE_CONTENT = settings.max_length_note_content # Default: 3000 (same as frontend)
