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

def test__convert_ltask_exception_exc_none(ltask_manager):
    with pytest.raises(AssertionError):
        ltask_manager._convert_ltask_exception(None)

def test__convert_ltask_exception_not_exception(ltask_manager, faker):
    with pytest.raises(AssertionError):
        ltask_manager._convert_ltask_exception(faker.word())

def test__convert_ltask_exception(ltask_manager, faker):
    message = faker.word()
    exc = ValueError(message)

    ltask_exception = ltask_manager._convert_ltask_exception(exc)
    assert ltask_exception.type == 'ValueError'
    assert ltask_exception.message == [message]

def test__convert_from_ltask_to_ltask_info(ltask_manager, faker):
    message = faker.word()
    exc = ValueError(message)
    result = {faker.word(): faker.word()}
    ltask = LTask(
        loop=None, ltask_manager=ltask_manager, coro=None
    )
    ltask._res = result
    ltask._exc = exc

    ltask_info: LTaskInfo = ltask_manager._convert_from_ltask_to_ltask_info(
        ltask_status=LTaskStatus.SUCCESS,
        ltask=ltask
    )

    assert ltask_info.status == LTaskStatus.SUCCESS
    assert ltask_info.result == result
    assert ltask_info.exc.type == 'ValueError'
    assert ltask_info.exc.message == [message]
    assert ltask_info.uuid == ltask.uuid


def test__convert_from_ltask_to_ltask_info_without_result_and_exception(ltask_manager, faker):
    ltask = LTask(
        loop=None, ltask_manager=ltask_manager, coro=None
    )

    ltask_info: LTaskInfo = ltask_manager._convert_from_ltask_to_ltask_info(
        ltask_status=LTaskStatus.PROCESS,
        ltask=ltask
    )

    assert ltask_info.status == LTaskStatus.PROCESS
    assert ltask_info.result == None
    assert ltask_info.exc == None
    assert ltask_info.uuid == ltask.uuid
