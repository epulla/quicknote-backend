import json
from datetime import datetime

from ...domain import NoteRepository, Note
from ...domain.exceptions import NoteNotFound
from ....shared.domain.exceptions import DBConnectionError

import redis.asyncio as async_redis
import redis


class RedisNoteRepository(NoteRepository):
    def __init__(self, host: str, port: int, password: str, ssl: bool):
        super().__init__("redis")
        self.conn = async_redis.Redis(
            host=host,
            port=port,
            password=password,
            ssl=ssl
        )

    async def create_note(self, note: Note, expiration_time: int):
        print("Saving note")
        await self.conn.set(note.id, json.dumps(note.__dict__, default=str), ex=expiration_time)
        print("Note saved")

    async def get_note_by_id(self, id: str) -> Note:
        print(f"Getting note with id: {id}")
        response = await self.conn.get(id)
        print(response)
        if response is None:
            raise NoteNotFound
        return Note(**json.loads(response))

    async def update_note_by_id(self, id: str, note: Note):
        print(f"Updating note with id: {id}")
        await self.get_note_by_id(id)
        await self._update_note_keeping_its_expiration_time(id, note)

    async def soft_delete_note(self, id: str):
        print(f"Soft deleting note with id: {id}")
        selected_note = await self.get_note_by_id(id)
        selected_note.content = ""
        selected_note.deleted = datetime.now()
        selected_note.current_view = selected_note.max_views
        await self._update_note_keeping_its_expiration_time(selected_note.id, selected_note)

    async def _update_note_keeping_its_expiration_time(self, id: str, note: Note):
        # 'keepttl' flag helps to keep the expiration time set in 'self.create_note' function
        await self.conn.set(id, json.dumps(note.__dict__, default=str), keepttl=True)

    async def check_connection(self):
        try:
            await self.conn.ping()
        except redis.exceptions.ConnectionError:
            raise DBConnectionError('redis')
