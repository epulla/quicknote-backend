from uuid import uuid4
from datetime import datetime

from .input_note import InputNote

from pydantic import BaseModel


class Note(BaseModel):
    id: str
    content: str
    max_views: int
    current_view: int = 0
    created: datetime = datetime.now()
    deleted: datetime = None

    @property
    def was_deleted(self):
        return not self.deleted is None

    @property
    def has_available_views(self):
        return self.current_view < self.max_views

    @classmethod
    def get_note_by_input_note(cls, input_note: InputNote):
        return Note(id=str(uuid4()), **input_note.__dict__)
