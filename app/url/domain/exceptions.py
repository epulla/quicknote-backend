

class UrlNotFound(Exception):
    """Raise when a URL is not found in the DB"""
    def __init__(self):
        self.message = "URL/Note not found"
        super().__init__(self.message)
