from datetime import datetime

from pydantic import BaseModel


class InputUrl(BaseModel):
    original_url: str
    expires_in: int  # in seconds
    deleted: datetime = None
