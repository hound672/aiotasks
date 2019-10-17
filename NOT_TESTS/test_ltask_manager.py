import asyncio
from unittest import mock

import pytest

from aiotasks._exceptions import LTaskNotFount
from aiotasks._typing import LTaskUuid
from aiotasks._ltask import LTask
from aiotasks._structs import LTaskStatus, LTaskInfo

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
            ltask_info = ltask_manager.create_ltask(_test_task())
            _task = ltask_manager._ltasks[ltask_info.uuid]
            await _task.wait()

            assert mocked.called

    event_loop.run_until_complete(run())


def test_ltask_execute(event_loop, ltask_manager): # TODO change tests'name
    async def _test_task():
        pass

    async def run():
        ltask_info = ltask_manager.create_ltask(_test_task())
        _task = ltask_manager._ltasks[ltask_info.uuid]
        assert ltask_info.uuid in ltask_manager._ltasks
        await _task.wait()
        assert ltask_info.uuid not in ltask_manager._ltasks

    event_loop.run_until_complete(run())

def test_cancel_task_not_found(event_loop, ltask_manager, faker): # TODO change tests'name
    async def run():
        pass

    with pytest.raises(LTaskNotFount):
        ltask_manager.cancel_ltask(LTaskUuid(faker.word()))

    event_loop.run_until_complete(run())

def test_cancel_task(event_loop, ltask_manager):
    async def _test_task():
        await asyncio.sleep(5)

    async def run():
        ltask_info = ltask_manager.create_ltask(_test_task())
        _task = ltask_manager._ltasks[ltask_info.uuid]
        ltask_manager.cancel_ltask(ltask_info.uuid)
        try:
            await _task.wait()
        except Exception:
            pass
        assert ltask_info.uuid not in ltask_manager._ltasks

    event_loop.run_until_complete(run())

# def test_create_task(event_loop, ltask_manager):
#     globals()['ltask_info'] = None
#     async def _test_task():
#         await asyncio.sleep(1)
#
#     async def _fake_write_task_info(self, ltask_info: LTaskInfo):
#         breakpoint()
#         assert globals()['ltask_info'] == ltask_info
#
#     async def run():
#         with mock.patch('aiotasks._backends._dummy.DummyBackend.write_task_info', new=_fake_write_task_info):
#             globals()['ltask_info'] = ltask_manager.create_ltask(_test_task())
#             await asyncio.sleep(1)
#
#
#     event_loop.run_until_complete(run())
