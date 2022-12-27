
from ..domain import NoteRepository, Note


class NoteReader:
    def __init__(self, note_repository: NoteRepository) -> None:
        self.note_repository = note_repository

    async def read_note_and_destroy(self, id: str) -> Note:
        read_note = await self.note_repository.get_note_by_id(id)
        read_note.current_view += 1
        if read_note.has_available_views:
            await self.note_repository.update_note_by_id(id, read_note)
        else:
            await self.note_repository.soft_delete_note(id)
            read_note.current_view = read_note.max_views
        return read_note
