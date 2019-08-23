import asyncio
from unittest import mock

import pytest

from aiotasks._ltask import LTask
from aiotasks._exceptions import LTaskNotStarted


class SomeException(Exception):
    pass

########################################################

def test_repr(event_loop, ltask_manager):
    async def _test_task():
        pass

    async def run():
        uuid_task = ltask_manager.create_ltask(_test_task())
        _task = ltask_manager._ltasks[uuid_task]
        _repr = f'<LTask: {uuid_task}>'
        assert _repr == repr(_task)

    event_loop.run_until_complete(run())


def test__task_done_called(event_loop, ltask_manager):

    async def _test_task():
        pass

    async def run():
        with mock.patch('aiotasks._ltask.LTask._task_done') as mocked:
            ltask_manager.create_ltask(_test_task())
            await asyncio.sleep(1)
            assert mocked.called

    event_loop.run_until_complete(run())


def test_wait_result(event_loop, ltask_manager, faker):
    task_result_value = faker.word()

    async def _test_task():
        await asyncio.sleep(1)
        return task_result_value

    async def run():
        ltask_uuid = ltask_manager.create_ltask(_test_task())
        _task = ltask_manager._ltasks[ltask_uuid]
        res = await _task.wait()
        assert res == task_result_value
        assert _task._done

    event_loop.run_until_complete(run())


def test_wait_exception(event_loop, ltask_manager, faker):
    async def _test_task():
        raise SomeException

    async def run():
        ltask_uuid = ltask_manager.create_ltask(_test_task())
        _task = ltask_manager._ltasks[ltask_uuid]
        with pytest.raises(SomeException):
            await _task.wait()

    event_loop.run_until_complete(run())

def test__task_done_result(event_loop, ltask_manager, faker):
    task_result_value = faker.word()

    async def _test_task():
        return task_result_value

    async def run():
        ltask_uuid = ltask_manager.create_ltask(_test_task())
        _task = ltask_manager._ltasks[ltask_uuid]
        await _task.wait()
        assert _task.res == task_result_value

    event_loop.run_until_complete(run())


def test__task_done_exception(event_loop, ltask_manager):
    async def _test_task():
        raise SomeException

    async def run():
        ltask_uuid = ltask_manager.create_ltask(_test_task())
        _task = ltask_manager._ltasks[ltask_uuid]
        try:
            await _task.wait()
        except:
            pass
        assert isinstance(_task.exc, SomeException)

    event_loop.run_until_complete(run())


def test_timeout_task(event_loop, ltask_manager):
    async def _test_task():
        await asyncio.sleep(5)

    async def run():
        uuid_task = ltask_manager.create_ltask(
            _test_task(),
            timeout=1
        )
        _task = ltask_manager._ltasks[uuid_task]
        with pytest.raises(asyncio.TimeoutError):
            await _task.wait()
        assert isinstance(_task.exc, asyncio.TimeoutError)
        assert _task.res is None

    event_loop.run_until_complete(run())

def test_cancel_error(event_loop, ltask_manager):
    async def _test_task():
        pass

    async def run():
        task = LTask(
            ltask_manager=ltask_manager,
            coro=_test_task(),
            loop=event_loop
        )
        with pytest.raises(LTaskNotStarted):
            task.cancel()

    event_loop.run_until_complete(run())


def test_cancel(event_loop, ltask_manager):
    async def _test_task():
        await asyncio.sleep(5)

    async def run():
        uuid_task = ltask_manager.create_ltask(
            _test_task()
        )
        _task = ltask_manager._ltasks[uuid_task]
        _task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await _task.wait()

        assert isinstance(_task.exc, asyncio.CancelledError)
        assert _task.res is None



    event_loop.run_until_complete(run())
