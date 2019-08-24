import asyncio
from abc import ABC, abstractmethod
from typing import Tuple

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
    async def connect(self) -> None:  # pragma: no cover
        pass

    @abstractmethod
    async def close(self) -> None:  # pragma: no cover
        pass

    @abstractmethod
    async def _write(self, key: str, value: dict) -> None:  # pragma: no cover
        pass

    @abstractmethod
    async def _read(self, key: str) -> dict:  # pragma: no cover
        """Should raise RecordNotFound exception if record was not found"""
        pass

    @staticmethod
    def _get_task_key(ltask_uuid: LTaskUuid) -> str:
        """Return ltask's key as it stores in backend"""
        return f'aiotasks-task-{ltask_uuid}'

    @staticmethod
    def _convert_from_ltask_info(ltask_info: LTaskInfo) -> Tuple[str, dict]:
        """Convert from LTaskInfo to key and value for write to backend"""
        key = BaseBackend._get_task_key(ltask_info.uuid)
        value = {
            'status': ltask_info.status.value,
            'result': ltask_info.result,
            'exc': ltask_info.exc
        }
        return key, value

    @staticmethod
    def _convert_to_ltask_info(ltask_uuid: LTaskUuid, value: dict) -> LTaskInfo:
        """Convert data from backend to LTaskInfo"""
        if not isinstance(value, dict):
            raise LTaskNotFount

        try:
            ltask_info = LTaskInfo(
                uuid=ltask_uuid,
                status=LTaskStatus(value['status']),
                result=value['result'],
                exc=value['exc']
            )
        except (ValueError, KeyError):
            raise LTaskNotFount

        return ltask_info

    async def write_task_info(self, ltask_info: LTaskInfo) -> None:
        """Convert LTaskInfo and write to backend"""
        key, value = BaseBackend._convert_from_ltask_info(ltask_info)
        await self._write(key=key, value=value)

    async def read_task_info(self, ltask_uuid: LTaskUuid) -> LTaskInfo:
        """
        Read task info from backend
        Raise LTaskNotFount if ltask was not found
        """
        key = BaseBackend._get_task_key(ltask_uuid)
        try:
            value = await self._read(key)
        except BaseBackend.RecordNotFound:
            raise LTaskNotFount

        return BaseBackend._convert_to_ltask_info(ltask_uuid, value)
