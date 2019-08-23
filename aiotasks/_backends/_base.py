import asyncio
from abc import ABC, abstractmethod

from .._structs import LTaskInfo, LTaskStatus
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
    async def connect(self) -> None:  #pragma: no cover
        pass

    @abstractmethod
    async def close(self) -> None:  #pragma: no cover
        pass

    @abstractmethod
    async def _write(self, key: str, value: dict) -> None:  #pragma: no cover
        pass

    @abstractmethod
    async def _read(self, key: str) -> dict:  #pragma: no cover
        pass

    async def write_task_info(self, ltask_info: LTaskInfo) -> None:
        """Convert LTaskInfo and write to backend"""
        key = str(ltask_info.uuid)
        value = {
            'status': ltask_info.status.value
        }
        await self._write(key=key, value=value)

    async def read_task_info(self, ltask_uuid: LTaskUuid) -> LTaskInfo:
        """
        Read task info from backend
        Raise LTaskNotFount is ltask was not found
        """
        try:
            data = await self._read(str(ltask_uuid))
        except BaseBackend.RecordNotFound:
            raise LTaskNotFount

        if not isinstance(data, dict):
            raise LTaskNotFount

        try:
            ltask_info = LTaskInfo(
                uuid=ltask_uuid,
                status=LTaskStatus(data['status'])
            )
        except (ValueError, KeyError):
            raise LTaskNotFount

        return ltask_info
