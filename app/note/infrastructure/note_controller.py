import typing
from ..domain import InputNote, NoteRepository, Note
from ..application import NoteReader, NoteCreator, NoteEncrypter


class NoteController:
    def __init__(self, note_repository: NoteRepository, note_encrypter: NoteEncrypter) -> None:
        self.note_repository = note_repository
        self.note_encrypter = note_encrypter

    async def create_note(self, input_note: InputNote) -> typing.Tuple[str, str, str, Note]:
        note_creator = NoteCreator(self.note_repository)
        key, tag, nonce, encrypted_input_note = self.note_encrypter.encrypt_note(input_note)
        created_note =  await note_creator.create_note(encrypted_input_note)
        return key, tag, nonce, created_note

    async def read_note_and_destroy(self, id: str, key: str, tag: str, nonce: str) -> Note:
        note_reader = NoteReader(self.note_repository)
        encrypted_note = await note_reader.read_note_and_destroy(id)
        if encrypted_note.was_deleted:
            return encrypted_note
        decrypted_note = self.note_encrypter.decrypt_note(key, tag, nonce, encrypted_note)
        return decrypted_note
