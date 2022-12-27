from uuid import uuid4
from datetime import datetime

from .input_url import InputUrl

from pydantic import BaseModel


class Url(BaseModel):
    id: str = str(uuid4())
    original_url: str
    deleted: datetime = None

    @classmethod
    def get_url_by_input_url(cls, input_url: InputUrl):
        return Url(id=str(uuid4()), **input_url.__dict__)
