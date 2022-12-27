import typing
from base64 import b64encode

from ..domain import InputNote, Note
from ...shared.domain import Encrypter


class NoteEncrypter:
    def __init__(self, encrypter: Encrypter) -> None:
        self.encrypter = encrypter

    def encrypt_note(self, input_note: InputNote) -> typing.Tuple[str, str, InputNote]:
        key, tag, nonce, encrypted_content = self.encrypter.encrypt(
            input_note.content
        )
        input_note.content = encrypted_content
        return key, tag, nonce, InputNote(**input_note.__dict__)

    def decrypt_note(self, key: str, tag: str, nonce: str, note: Note) -> Note:
        decrypted_content = self.encrypter.decrypt(key, tag, nonce, note.content)
        note.content = decrypted_content
        return Note(**note.__dict__)
