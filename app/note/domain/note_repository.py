from abc import ABC, abstractmethod, abstractproperty

from .note import Note


class NoteRepository(ABC):
    def __init__(self, db_type: str):
        self.db_type = db_type

    @abstractmethod
    async def create_note(self, note: Note, expiration_time: str):
        """This method will create a register of a Note that can expire (in seconds)"""
        pass

    @abstractmethod
    async def get_note_by_id(self, id: str) -> Note:
        """This method will get a register of a Note"""
        pass

    @abstractmethod
    async def update_note_by_id(self, id: str, note: Note):
        """This method will update a note by its id"""
        pass

    @abstractmethod
    async def soft_delete_note(self, id: str):
        """This method will remove the content of a Note and update its deleted date and state as inactive"""
        pass

    @abstractmethod
    async def check_connection(self):
        """This method checks the connection to the DB, if the connection fails, a ConnectionError will raise"""
