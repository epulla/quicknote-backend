import asyncio
import typing
import time
from datetime import datetime

from ...domain import Note, NoteRepository
from ...domain.exceptions import NoteNotFound

from anyio import sleep
from pydantic import BaseModel

DUMMY_DELAY = 0.5  # Time delay of each response from the dummy repository


class DummyNoteRepository(NoteRepository):
    def __init__(self):
        super().__init__("python-dictionary")
        self.db: typing.Dict = {}

    async def create_note(self, note: Note, expiration_time: int):
        # Create async worker threads (one for creating and another for deleting a Note)
        workers = [self._create_note(note), self._hard_delete_note(
            note.id, expiration_time)]
        asyncio.gather(*workers)

    async def _create_note(self, note: Note):
        print(f"Saving note")
        await sleep(0.5)
        self.db[note.id] = note
        print(f"Note saved")
        print(f"db: {self.db}")

    async def _hard_delete_note(self, id: str, expiration_time: int):
        try:
            await sleep(expiration_time)
            print(f'Hard deleting of Note with id {id}')
            self.db.pop(id)
        except KeyError:
            raise NoteNotFound

    async def get_note_by_id(self, id: str) -> Note:
        print(f"Getting note with id: {id}")
        await sleep(0.5)
        try:
            selected_note = self.db[id]
        except KeyError:
            raise NoteNotFound
        return Note(**selected_note.__dict__)

    async def update_note_by_id(self, id: str, note: Note):
        print(f"Updating note with id: {id}")
        await self.get_note_by_id(id)
        print(self.db)
        print(note)
        self.db[id] = Note(**note.__dict__)

    async def soft_delete_note(self, id: str):
        print(f'Soft deleting note with id: {id}')
        await sleep(0.5)
        selected_note = self.db[id]
        selected_note.content = ""
        selected_note.deleted = datetime.now()
        selected_note.current_view = selected_note.max_views
        print(f'Note content was removed at {selected_note.deleted}')

    async def check_connection(self):
        pass
