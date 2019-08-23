import asyncio
from unittest import mock

def test_create_ltask(event_loop, ltask_manager):

    async def _test_task():
        pass

    async def run():
        await ltask_manager.create_ltask(_test_task())
        assert len(ltask_manager) == 1
        assert (len(ltask_manager._ltasks)) == 1
        await asyncio.sleep(1)

    event_loop.run_until_complete(run())


def test_ltask_done_called(event_loop, ltask_manager):

    async def _test_task():
        pass

    async def _fake(self=None, result=None, exc=None):
        pass

    async def run():
        with mock.patch('aiotasks._ltask_manager.LTaskManager.ltask_done', return_value=_fake()) as mocked:
            await ltask_manager.create_ltask(_test_task())
            await asyncio.sleep(1)
            assert mocked.called

    event_loop.run_until_complete(run())


def test_ltask_execute(event_loop, ltask_manager): # TODO change tests'name

    async def _test_task():
        pass

    async def run():
        ltask_uuid = await ltask_manager.create_ltask(_test_task())
        assert ltask_uuid in ltask_manager._ltasks
        await asyncio.sleep(1)
        assert ltask_uuid not in ltask_manager._ltasks

    event_loop.run_until_complete(run())
