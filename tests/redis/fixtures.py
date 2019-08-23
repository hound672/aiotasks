import pytest
import aioredis

from aiotasks._backends._redis import RedisBackend

@pytest.fixture
def get_redis_url():
    host = '192.168.140.129'
    port = 6379
    db = '0'

    return f'redis://{host}:{port}/{db}'

@pytest.fixture
def redis_backend(event_loop, get_redis_url):
    """Return redis backend"""

    async def run():
        backend = RedisBackend(
            loop=event_loop,
            url=get_redis_url
        )
        await backend.connect()
        return backend

    backend = event_loop.run_until_complete(run())
    yield backend

    async def run_after():
        await backend.close()

    event_loop.run_until_complete(run_after())

@pytest.fixture
def redis_client(event_loop, get_redis_url):
    """Return redis client"""
    async def run():
        return await aioredis.create_redis(
            get_redis_url,
                loop=event_loop
            )

    _redis_client = event_loop.run_until_complete(run())
    yield _redis_client

    async def run_after():
        await _redis_client.flushdb()
        _redis_client.close()

    event_loop.run_until_complete(run_after())
