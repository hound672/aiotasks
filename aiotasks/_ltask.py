import asyncio
import uuid
import typing
from typing import Coroutine, Any, Optional

if typing.TYPE_CHECKING:
    from ._ltask_manager import LTaskManager

class LTask:
    """Class wrapper for asyncio tasks"""

    _task: Optional[asyncio.tasks.Task] = None

    def __init__(self, *,
                 ltask_manager: 'LTaskManager',
                 coro: Coroutine[Any, Any, Any],
                 loop: asyncio.AbstractEventLoop,
                 timeout: int # TODO !!!
                 ) -> None:
        """
        :param ltask_manager: Main TaskManager
        :param coro: coro for task
        :param loop: base event loop
        """
        self._ltask_manager = ltask_manager
        self._uuid = uuid.uuid4().hex
        self._coro = coro
        self._loop = loop
        self._timeout = timeout

    @property
    def uuid(self) -> str:
        return self._uuid

    def __repr__(self) -> str:
        return f'<LTask: {self._uuid}>'

    async def start(self):
        """Start coro as task"""
        assert self._task is None

        # with _wrap we are able to have async done_callback
        async def _wrap():
            res, exc = None, None
            try:
                res = await self._coro
            except Exception as e:
                print(type(e))
                exc = e
            finally:
                await self._task_done(res, exc)

        self._task = asyncio.create_task(
            asyncio.wait_for(_wrap(), self._timeout)
        )

    async def _task_done(self, result: Any, exc: Any):  # FIXME exc have to have type
        print(f'Task is done. Res: {result}. exc: {exc}')


########################################################

class TClass:
    async def method_1(self):
        return await self.method_2()

    async def method_2(self):
        return 123

async def func1():
    return 123

async def func2():
    res = await func1()
    return res