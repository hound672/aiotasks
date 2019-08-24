import json

import aioredis

from ._base import BaseBackend
from .._exceptions import ErrorConnectBackend


class RedisBackend(BaseBackend):

    async def connect(self) -> None:
        try:
            self._redis = await aioredis.create_redis(
                self._url,
                loop=self._loop
            )
        except Exception:
            raise ErrorConnectBackend

    async def close(self) -> None:
        self._redis.close()  # pragma: no cover

    async def _write(self, key: str, value: dict) -> None:
        data = json.dumps(value)
        await self._redis.set(key=key, value=data)

    async def _read(self, key: str) -> dict:
        data = await self._redis.get(key=key)
        try:
            return json.loads(data)
        except (json.JSONDecodeError, TypeError):
            raise BaseBackend.RecordNotFound
