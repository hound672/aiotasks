import asyncio
from abc import ABC, abstractmethod
from typing import Tuple

from .._structs import LTaskInfo, LTaskStatus, LTaskException
from .._typing import LTaskUuid
from .._exceptions import LTaskNotFount


class BaseBackend(ABC):
    """Base class for Backend"""

    class RecordNotFound(Exception):
        pass

    def __init__(self, *,
                 loop: asyncio.AbstractEventLoop,
                 url: str
                 ) -> None:
        self._loop = loop
        self._url = url

    @abstractmethod
    async def connect(self) -> None:  # pragma: no cover
        """Should raise ErrorConnectBackend exception if connection if fault"""
        pass

    @abstractmethod
    async def close(self) -> None:  # pragma: no cover
        pass

    @abstractmethod
    async def _write(self, key: str, data: dict) -> None:  # pragma: no cover
        pass

    @abstractmethod
    async def _read(self, key: str) -> dict:  # pragma: no cover
        """Should raise RecordNotFound exception if record was not found"""
        pass

    @staticmethod
    def _get_task_key(ltask_uuid: LTaskUuid) -> str:
        """Return ltask's key as it stores in backend"""
        return f'aiotasks-task-{ltask_uuid}'

    async def write_task_info(self, ltask_info: LTaskInfo) -> None:
        """Convert LTaskInfo and write to backend"""
        _, data = ltask_info.to_backend()
        key = BaseBackend._get_task_key(ltask_uuid=ltask_info.uuid)
        await self._write(key=key, data=data)

    async def read_task_info(self, ltask_uuid: LTaskUuid) -> LTaskInfo:
        """
        Read task info from backend
        Raise LTaskNotFount if ltask was not found
        """
        key = BaseBackend._get_task_key(ltask_uuid)
        try:
            data = await self._read(key)
        except BaseBackend.RecordNotFound:
            raise LTaskNotFount

        return LTaskInfo.from_backend(ltask_uuid=ltask_uuid, data=data)
