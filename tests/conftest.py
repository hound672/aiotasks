import pytest

from faker import Factory

from aiotasks._ltask_manager import LTaskManager


pytest_plugins = ['tests.redis.fixtures']

@pytest.fixture
def faker():
    """Faker object"""
    return Factory.create()

@pytest.fixture
def ltask_manager(event_loop):
    """Return LTaskManager instance"""
    async def run():
        return await LTaskManager.create_ltask_manager(
            back_end_url=''
        )

    yield event_loop.run_until_complete(run())


@pytest.fixture
def ltask_manager_redis(event_loop):
    """Return LTaskManager instance with Redis backend"""

    _host = '192.168.140.129'
    _port = 6379

    async def run():
        return await LTaskManager.create_ltask_manager(
            back_end_url=f'redis//{_host}:{_port}'
        )

    yield event_loop.run_until_complete(run())
