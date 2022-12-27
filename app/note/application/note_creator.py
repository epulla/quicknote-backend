from ..domain import Note, InputNote, NoteRepository
from ..domain.exceptions import ExceededMaxNoteLength, EmptyNote

from ...shared.constants import MAX_LENGTH_NOTE_CONTENT


class NoteCreator:
    def __init__(self, note_repository: NoteRepository) -> None:
        self.note_repository = note_repository

    async def create_note(self, input_note: InputNote) -> Note:
        if len(input_note.content) == 0:
            raise EmptyNote
        if len(input_note.content) >= MAX_LENGTH_NOTE_CONTENT:
            raise ExceededMaxNoteLength
        created_note = Note.get_note_by_input_note(input_note)
        await self.note_repository.create_note(created_note, input_note.expires_in)
        return created_note
