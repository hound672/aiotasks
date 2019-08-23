import asyncio
from unittest import mock

import pytest

from aiotasks._exceptions import LTaskNotFount
from aiotasks._typing import LTaskUuid

def test_create_ltask(event_loop, ltask_manager):

    async def _test_task():
        pass

    async def run():
        ltask_manager.create_ltask(_test_task())
        assert len(ltask_manager) == 1
        assert (len(ltask_manager._ltasks)) == 1

    event_loop.run_until_complete(run())


def test_ltask_done_called(event_loop, ltask_manager):

    async def _test_task():
        pass

    async def run():
        with mock.patch('aiotasks._ltask_manager.LTaskManager._ltask_done') as mocked:
            ltask_manager.create_ltask(_test_task())
            ltask_uuid = ltask_manager.create_ltask(_test_task())
            _task = ltask_manager._ltasks[ltask_uuid]
            await _task.wait()

            assert mocked.called

    event_loop.run_until_complete(run())


def test_ltask_execute(event_loop, ltask_manager): # TODO change tests'name
    async def _test_task():
        pass

    async def run():
        ltask_uuid = ltask_manager.create_ltask(_test_task())
        _task = ltask_manager._ltasks[ltask_uuid]
        assert ltask_uuid in ltask_manager._ltasks
        await _task.wait()
        assert ltask_uuid not in ltask_manager._ltasks

    event_loop.run_until_complete(run())

def test_cancel_task_not_found(event_loop, ltask_manager, faker): # TODO change tests'name
    async def run():
        pass

    with pytest.raises(LTaskNotFount):
        ltask_manager.cancel_task(LTaskUuid(faker.word()))

    event_loop.run_until_complete(run())

def test_cancel_task(event_loop, ltask_manager):
    async def _test_task():
        await asyncio.sleep(5)

    async def run():
        ltask_uuid = ltask_manager.create_ltask(_test_task())
        _task = ltask_manager._ltasks[ltask_uuid]
        ltask_manager.cancel_task(ltask_uuid)
        try:
            await _task.wait()
        except Exception:
            pass
        assert ltask_uuid not in ltask_manager._ltasks

    event_loop.run_until_complete(run())
