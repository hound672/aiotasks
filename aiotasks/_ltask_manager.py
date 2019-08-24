import asyncio
from typing import Coroutine, Any, Dict, Optional

from ._backends._base import BaseBackend
from ._ltask import LTask
from ._typing import LTaskUuid
from ._exceptions import LTaskNotFount
from ._helpers import get_backend_by_url
from ._structs import LTaskStatus, LTaskInfo, LTaskException

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

    @staticmethod
    def _convert_ltask_exception(exc: Exception) -> LTaskException:
        """Convert Exception instance to internal LTaskException instance"""
        assert isinstance(exc, Exception), 'exc have to be Exception instance'
        return LTaskException(
            type=type(exc).__name__,
            message=[i for i in exc.args]
        )

    @staticmethod
    def _convert_from_ltask_to_ltask_info(*,
                                          ltask_status: LTaskStatus,
                                          ltask: LTask) -> LTaskInfo:
        """Convert LTask to LTaskInfo for later written to backend"""
        return LTaskInfo(
            status=ltask_status,
            uuid=ltask.uuid,
            result=ltask.res,
            exc=LTaskManager._convert_ltask_exception(ltask.exc)
        )
        return ltask_info

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
