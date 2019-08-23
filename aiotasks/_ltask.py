import asyncio
import uuid
import typing
from typing import Coroutine, Any, Optional

if typing.TYPE_CHECKING:
    from ._ltask_manager import LTaskManager  # pragma: no cover

from ._exceptions import LTaskNotStarted

class LTask:
    """Class wrapper for asyncio tasks"""

    _task: Optional[asyncio.tasks.Task] = None
    _done: bool = False
    _res: Optional[Any] = None
    _exc: Optional[Exception] = None

    def __init__(self, *,
                 ltask_manager: 'LTaskManager',
                 coro: Coroutine[Any, Any, Any],
                 loop: asyncio.AbstractEventLoop,
                 timeout: Optional[int] = None
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

    @property
    def res(self) -> Optional[Any]:
        return self._res

    @property
    def exc(self) -> Optional[Exception]:
        return self._exc

    def __repr__(self) -> str:
        return f'<LTask: {self._uuid}>'

    async def wait(self) -> Optional[Any]:
        """Wait for task"""
        try:
            return await self._task  # type: ignore
        except Exception:
            raise

    def start(self) -> None:
        """Start coro as task"""
        assert self._task is None

        self._task = asyncio.create_task(
            asyncio.wait_for(self._coro, self._timeout)
        )
        self._task.add_done_callback(self._task_done)

    def cancel(self) -> None:
        """Cancel current task"""
        if self._task is None:
            raise LTaskNotStarted
        self._task.cancel()

    def _task_done(self, task: asyncio.Task) -> None:
        self._done = True
        try:
            self._res = task.result()
        except Exception as e:
            self._exc = e
        self._ltask_manager._ltask_done(self)
