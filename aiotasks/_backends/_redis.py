import asyncio

import aioredis

from aiotasks._structs import LTaskInfo
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

    # async def _write_task_info(self, task_info: LTaskInfo) -> None:
    #     pass
