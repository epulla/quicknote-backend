import typing

from ...shared.domain import StrEncoder
from ...shared.domain.exceptions import UrlWithMoreParamsAsExpected


class UrlEncoder:
    def __init__(self, str_encoder: StrEncoder):
        self.str_encoder = str_encoder

    def encode_many_to_url(self, params: typing.List[str], separator: str) -> str:
        joined_data = separator.join(params)
        return self.str_encoder.encode_str(joined_data)

    def decode_many_to_url(self, encoded_url: str, separator: str, limit: int) -> typing.Tuple[str, ...]:
        decoded_url = self.str_encoder.decode_str(encoded_url)
        split_params = decoded_url.split(separator)
        if len(split_params) != limit:
            raise UrlWithMoreParamsAsExpected
        return tuple(split_params)
