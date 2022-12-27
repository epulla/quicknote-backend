from ...shared.constants import MAX_LENGTH_NOTE_CONTENT


class NoteNotFound(Exception):
    """Raised when a note is not found in the DB"""

    def __init__(self):
        self.message = "Note not found"
        super().__init__(self.message)


class EmptyNote(Exception):
    """Raised when a note is empty"""

    def __init__(self):
        self.message = "Empty note"
        super().__init__(self.message)


class ExceededMaxNoteLength(Exception):
    """Raised when a note has exceeded the max amount of chars"""

    def __init__(self):
        self.message = f"Not has exceeded the limit of {MAX_LENGTH_NOTE_CONTENT}"
        super().__init__(self.message)
