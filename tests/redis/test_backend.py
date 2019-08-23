import pytest
import random
import uuid

from aiotasks._typing import LTaskUuid
from aiotasks._exceptions import ErrorConnectBackend
from aiotasks._structs import LTaskInfo, LTaskStatus


def Ntest_error_connect(event_loop, redis_backend, faker):
    async def run():
        redis_backend._url = f'redis://{faker.ipv4_public()}:{faker.random_int()}/{faker.random_int()}'
        with pytest.raises(ErrorConnectBackend):
            await redis_backend.connect()

    event_loop.run_until_complete(run())

def Ntest_write_ltask_info(event_loop, redis_backend, faker, redis_client):
    ltask = LTaskInfo(
        uuid=LTaskUuid(uuid.uuid4().hex),
        status=random.choice(list(LTaskStatus))
    )

    async def run():
        val = await redis_client.get('key')

        breakpoint()

    event_loop.run_until_complete(run())


