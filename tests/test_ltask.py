import asyncio
from unittest import mock

import pytest


class SomeException(Exception):
    pass

########################################################

def test_repr(event_loop, ltask_manager):
    async def _test_task():
        pass

    async def run():
        uuid_task = await ltask_manager.create_ltask(_test_task())
        _task = ltask_manager._ltasks[uuid_task]
        _repr = f'<LTask: {uuid_task}>'
        assert _repr == repr(_task)

    event_loop.run_until_complete(run())


def test_wait_result(event_loop, ltask_manager, faker):
    task_result_value = faker.word()

    async def _test_task():
        await asyncio.sleep(1)
        return task_result_value

    async def run():
        uuid_task = await ltask_manager.create_ltask(_test_task())
        _task = ltask_manager._ltasks[uuid_task]
        res = await _task.wait()
        assert res == task_result_value

    event_loop.run_until_complete(run())


def test_wait_exception(event_loop, ltask_manager, faker):
    async def _test_task():
        raise ValueError

    async def run():
        uuid_task = await ltask_manager.create_ltask(_test_task())
        _task = ltask_manager._ltasks[uuid_task]
        with pytest.raises(ValueError):
            await _task.wait()

    event_loop.run_until_complete(run())


def test__task_done_called(event_loop, ltask_manager):

    async def _test_task():
        pass

    async def _fake(self=None, result=None, exc=None):
        pass

    async def run():
        with mock.patch('aiotasks._ltask.LTask._task_done', return_value=_fake()) as mocked:
            await ltask_manager.create_ltask(_test_task())
            await asyncio.sleep(1)
            assert mocked.called

    event_loop.run_until_complete(run())


def test__task_done_result(event_loop, ltask_manager, faker):
    task_result_value = faker.word()

    async def _test_task():
        return task_result_value

    async def _fake(self, result, exc):
        globals()['task_result'] = result

    async def run():

        with mock.patch('aiotasks._ltask.LTask._task_done', new=_fake) as mocked:
            await ltask_manager.create_ltask(_test_task())
            await asyncio.sleep(1)
            assert globals()['task_result'] == task_result_value

    event_loop.run_until_complete(run())


def test__task_done_exception(event_loop, ltask_manager, faker):

    async def _test_task():
        raise SomeException

    async def _fake(self, result, exc):
        globals()['task_exc'] = exc

    async def run():

        with mock.patch('aiotasks._ltask.LTask._task_done', new=_fake) as mocked:
            await ltask_manager.create_ltask(_test_task())
            await asyncio.sleep(1)
            assert isinstance(globals()['task_exc'], SomeException)

    event_loop.run_until_complete(run())
