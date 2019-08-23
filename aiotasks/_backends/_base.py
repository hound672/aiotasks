import asyncio
from abc import ABC, abstractmethod

from .._structs import LTaskInfo

class BaseBackend(ABC):
    """Base class for Backend"""

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
    async def _write(self, key: str, value: dict) -> None:  #pragma: no cover
        pass

    async def write_task_info(self, ltask_info: LTaskInfo) -> None:
        """Convert LTaskInfo and write to backend"""
        key = str(ltask_info.uuid)
        value = {
            'status': ltask_info.status.value
        }
        await self._write(key=key, value=value)
