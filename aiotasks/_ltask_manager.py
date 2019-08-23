import asyncio
from typing import Coroutine, Any, Dict, Optional

from ._ltask import LTask
from .backends._base import BaseBackend


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
        self._ltasks: Dict[str, LTask] = {}

    def __len__(self):
        return len(self._ltasks)

    @classmethod
    async def create_ltask_manager(cls, *,
                                   limit_active_ltasks: int = 10
                                   ) -> 'LTaskManager':
        """Create new instance of LTaskManager"""
        loop = asyncio.get_event_loop()
        backend = None # TODO !!!
        return cls(
            loop=loop,
            backend=backend,
            limit_active_ltasks = limit_active_ltasks
        )


    async def create_ltask(self,
                           coro: Coroutine[Any, Any, Any],
                           timeout: Optional[int] = None) -> str:
        """Create ltask from coroutine"""
        ltask = LTask(
            ltask_manager=self,
            coro=coro,
            loop=self._loop,
            timeout=timeout
        )
        self._ltasks[ltask.uuid] = ltask
        await ltask.start()

        return ltask.uuid

    async def _ltask_done(self, ltask: LTask):
        self._ltasks.pop(ltask.uuid)
