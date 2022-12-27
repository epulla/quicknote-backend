from base64 import b64encode, b64decode

from ..domain import StrEncoder

STR_ENCODE = 'utf-8'


class Base64StrEncoder(StrEncoder):
    def encode_str(self, message: str) -> str:
        message_bytes = message.encode(STR_ENCODE)
        base64_bytes = b64encode(message_bytes)
        return base64_bytes.decode(STR_ENCODE)

    def decode_str(self, encoded_message: str) -> str:
        base64_bytes = encoded_message.encode(STR_ENCODE)
        message_bytes = b64decode(base64_bytes)
        return message_bytes.decode(STR_ENCODE)
