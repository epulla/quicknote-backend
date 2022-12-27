import typing
from abc import ABC, abstractmethod


class Encrypter(ABC):
    @abstractmethod
    def encrypt(self, data: str) -> typing.Tuple[str, str, str, str]:
        """Encrypt data and return its key, tag and encrypted_data"""
        pass

    @abstractmethod
    def decrypt(self, key: str, tag: str, nonce: str, encrypted_data: str) -> str:
        """Decrypt encrypted data using key, tag"""
        pass
