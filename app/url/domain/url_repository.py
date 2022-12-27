from .url import Url

from abc import ABC, abstractmethod


class UrlRepository(ABC):
    def __init__(self, db_type: str):
        self.db_type = db_type

    @abstractmethod
    async def save_url(self, url: Url, expiration_time: int):
        """Save the URL into the DB"""
        pass

    @abstractmethod
    async def get_original_url(self, id: str) -> Url:
        """Get the original URL from the DB"""
        pass

    @abstractmethod
    async def check_connection(self):
        """This method checks the connection to the DB, if the connection fails, a ConnectionError will raise"""
