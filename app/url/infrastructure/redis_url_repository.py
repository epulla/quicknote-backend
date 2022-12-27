
import json

from ..domain import UrlRepository, Url
from ..domain.exceptions import UrlNotFound
from ...shared.domain.exceptions import DBConnectionError

import redis.asyncio as async_redis
import redis


class RedisUrlRepository(UrlRepository):
    def __init__(self, url: str):
        super().__init__("redis")
        self.conn = async_redis.from_url(url=url)

    async def save_url(self, url: Url, expiration_time: int):
        print("Saving URL")
        await self.conn.set(url.id, json.dumps(url.__dict__, default=str), ex=expiration_time)
        print("URL saved")

    async def get_original_url(self, id: str) -> Url:
        print(f"Getting original URL with id: {id}")
        response = await self.conn.get(id)
        if response is None:
            raise UrlNotFound
        return Url(**json.loads(response))

    async def check_connection(self):
        try:
            await self.conn.ping()
        except redis.exceptions.ConnectionError:
            raise DBConnectionError('redis')
