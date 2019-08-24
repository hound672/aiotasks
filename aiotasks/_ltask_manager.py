import asyncio
from typing import Coroutine, Any, Dict, Optional

from ._backends._base import BaseBackend
from ._ltask import LTask
from ._typing import LTaskUuid
from ._exceptions import LTaskNotFount
from ._helpers import get_backend_by_url

class LTaskManager:
    """Manger for tasks"""

    def __init__(self, *,
                 loop: asyncio.AbstractEventLoop,
                 backend: BaseBackend,
                 limit_active_ltasks: int
                 ) -> None:
        """
        :param limit_active_ltasks: max count active tasks at the same time
        """
        self._loop = loop
        self._backend = backend
        self._limit_active_ltasks = limit_active_ltasks
        self._ltasks: Dict[LTaskUuid, LTask] = {}

    def __len__(self) -> int:
        return len(self._ltasks)

    @classmethod
    async def create_ltask_manager(cls, *,
                                   limit_active_ltasks: int = 10,
                                   back_end_url: str
                                   ) -> 'LTaskManager':
        """Create new instance of LTaskManager"""
        loop = asyncio.get_event_loop()
        backend_cls = get_backend_by_url(back_end_url)
        backend = backend_cls(
            loop=loop,
            url=back_end_url
        )
        await backend.connect()
        return cls(
            loop=loop,
            backend=backend,
            limit_active_ltasks=limit_active_ltasks
        )

    def create_ltask(self,
                     coro: Coroutine[Any, Any, Any],
                     timeout: Optional[int] = None) -> LTaskUuid:
        """Create ltask from coroutine"""
        ltask = LTask(
            ltask_manager=self,
            coro=coro,
            loop=self._loop,
            timeout=timeout
        )
        self._ltasks[ltask.uuid] = ltask
        # TODO write to backend ltasks's info
        ltask.start()

        return ltask.uuid

    def cancel_task(self, ltask_uuid: LTaskUuid) -> None:
        """Cancel ltask by its uuid"""
        try:
            ltask = self._ltasks[ltask_uuid]
        except KeyError:
            raise LTaskNotFount

        ltask.cancel()

    def _ltask_done(self, ltask: LTask) -> None:
        self._ltasks.pop(ltask.uuid)
