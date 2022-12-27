import typing
from base64 import b64encode, b64decode

from ..domain import Encrypter

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

AES_KEY_BYTES_LENGTH = 32
AES_MODE = AES.MODE_GCM


class AESEncrypter(Encrypter):
    def encrypt(self, data: str) -> typing.Tuple[str, str, str, str]:
        key = get_random_bytes(AES_KEY_BYTES_LENGTH)
        cipher = AES.new(key, AES_MODE)
        encrypted_data, tag = cipher.encrypt_and_digest(data.encode())
        key_str, tag_str, nonce_str, encrypted_data_str = self._turn_bytes_into_str(
            [key, tag, cipher.nonce, encrypted_data]
        )
        return key_str, tag_str, nonce_str, encrypted_data_str

    def decrypt(self, key: str, tag: str, nonce: str, encrypted_data: str) -> str:
        key_bytes, tag_bytes, nonce_bytes, encrypted_data_bytes = self._turn_str_into_bytes(
            [key, tag, nonce, encrypted_data]
        )
        cipher = AES.new(key_bytes, AES_MODE, nonce=nonce_bytes)
        return cipher.decrypt_and_verify(encrypted_data_bytes, tag_bytes)

    def _turn_bytes_into_str(self, bytes_list: typing.List[bytes]) -> typing.List[str]:
        return tuple(b64encode(x).decode() for x in bytes_list)

    def _turn_str_into_bytes(self, str_list: typing.List[str]) -> typing.List[bytes]:
        return tuple(b64decode(x) for x in str_list)
