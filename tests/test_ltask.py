import asyncio
from unittest import mock

def test__task_done_called(ltask_manager, event_loop):

    async def _fake_coro():
        pass

    async def _fake_task_done(self = None, result = None, exc = None):
        pass

    async def run():
        with mock.patch('aiotasks._ltask.LTask._task_done') as mocked:
            await ltask_manager.create_ltask(_fake_coro())
            await asyncio.sleep(1)
            assert mocked.called

    event_loop.run_until_complete(run())
