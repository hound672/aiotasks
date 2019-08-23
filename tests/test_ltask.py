import asyncio
from unittest import mock

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
