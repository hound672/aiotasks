import pytest

from faker import Factory

from aiotasks._ltask_manager import LTaskManager

@pytest.fixture
def faker():
    """Faker object"""
    return Factory.create()

@pytest.fixture
def ltask_manager(event_loop):
    """Return LTaskManager instance"""
    async def run():
        return await LTaskManager.create_ltask_manager()

    yield event_loop.run_until_complete(run())
