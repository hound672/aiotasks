import logging
import asyncio
from typing import Coroutine, Any, Dict, Optional

from ._backends._base import BaseBackend
from ._ltask import LTask
from ._typing import LTaskUuid
from ._exceptions import LTaskNotFount
from ._helpers import get_backend_by_url
from ._structs import LTaskStatus, LTaskInfo, LTaskException


logger = logging.getLogger(__name__)

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

    def _write_task_info(self, ltask_info: LTaskInfo) -> None:
        """Create task for write LTaskInfo to backend"""
        asyncio.create_task(self._backend.write_task_info(ltask_info=ltask_info))

    def _ltask_done(self, ltask: LTask) -> None:
        """Callback called when task if finished"""
        ltask = self._ltasks[ltask.uuid]
        ltask_status = LTaskStatus.SUCCESS if ltask.res is not None else LTaskStatus.FAILURE
        ltask_info = LTaskInfo.from_ltask(ltask_status=ltask_status, ltask=ltask)

        logger.debug(f'Task done. Task: {ltask_info}')
        self._write_task_info(ltask_info)

        self._ltasks.pop(ltask.uuid)

    @classmethod
    async def create_ltask_manager(cls, *,
                                   limit_active_ltasks: int = 10,
                                   back_end_url: str
                                   ) -> 'LTaskManager':
        """Create new instance of LTaskManager"""
        logger.debug('Create LTaskManager')
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
                     timeout: Optional[int] = None) -> LTaskInfo:
        """Create ltask from coroutine"""
        ltask = LTask(
            ltask_manager=self,
            coro=coro,
            loop=self._loop,
            timeout=timeout
        )

        self._ltasks[ltask.uuid] = ltask
        ltask_info = LTaskInfo.from_ltask(ltask_status=LTaskStatus.PROCESS, ltask=ltask)
        self._write_task_info(ltask_info)

        should_start = True  # TODO task maybe goes to queue and not running
        if should_start:
            ltask.start()
        logger.debug(f'Task create. Start: {should_start}. Task: {ltask_info}')

        return ltask_info

    def cancel_ltask(self, ltask_uuid: LTaskUuid) -> None:
        """Cancel ltask by its uuid"""
        try:
            ltask = self._ltasks[ltask_uuid]
        except KeyError:
            raise LTaskNotFount

        ltask.cancel()

    async def get_ltask_info(self, ltask_uuid: LTaskUuid) -> LTaskInfo:
        """Return LTaskInfo instance about required task
        or raise LTaskNotFount if tsk was not found"""
        return await self._backend.read_task_info(ltask_uuid=ltask_uuid)
