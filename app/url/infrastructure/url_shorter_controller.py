from ..domain import UrlRepository, InputUrl, Url
from ...shared.domain import StrEncoder


class UrlShorterController:
    def __init__(self, url_repository: UrlRepository, str_encoder: StrEncoder):
        self.url_repository = url_repository
        self.str_encoder = str_encoder

    async def create_short_url(self, input_url: InputUrl) -> str:
        created_url = Url.get_url_by_input_url(input_url)
        await self.url_repository.save_url(created_url, expiration_time=input_url.expires_in)
        return self.str_encoder.encode_str(created_url.id)

    async def get_original_url(self, shorted_url: str) -> str:
        url_id = self.str_encoder.decode_str(shorted_url)
        selected_url = await self.url_repository.get_original_url(url_id)
        return selected_url.original_url
