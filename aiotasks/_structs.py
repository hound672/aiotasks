from dataclasses import dataclass
from enum import Enum, auto
from typing import Tuple, Dict, Optional, List

from pydantic import BaseModel, ValidationError

from ._typing import LTaskUuid, LTaskResult
from ._ltask import LTask


class LTaskStatus(Enum):
    def _generate_next_value_(name, start, count, last_values):  # type: ignore
        return name

    PROCESS = auto()
    SUCCESS = auto()
    FAILURE = auto()


class LTaskException(BaseModel):
    type: str
    message: List[str]


class LTaskInfo(BaseModel):
    uuid: LTaskUuid
    status: LTaskStatus
    result: Optional[LTaskResult] = None
    exc: Optional[LTaskException] = None

    class InvalidFormat(Exception):
        pass

    @classmethod
    def from_ltask(cls, *,
                   ltask_status: LTaskStatus,
                   ltask: LTask) -> 'LTaskInfo':
        """Create LTask instance from LTask instance"""
        exc = None
        if isinstance(ltask.exc, Exception):
            exc = LTaskException(
                type=type(ltask.exc).__name__,
                message=[i for i in ltask.exc.args]
            )

        return LTaskInfo(
            uuid=ltask.uuid,
            status=ltask_status,
            result=ltask.res,
            exc=exc
        )

    def to_backend(self) -> Tuple[LTaskUuid, Dict]:
        """Convert LTaskInfo to Tuple with ltask's uuid and data to backend"""
        data = {
            'status': self.status.value,
            'result': self.result,
            'exc': None if self.exc is None else self.exc.__dict__
        }
        return self.uuid, data

    @classmethod
    def from_backend(cls, *,
                     ltask_uuid: LTaskUuid,
                     data: Dict) -> 'LTaskInfo':
        """Create LTaskInfo from backend's data"""
        try:
            return LTaskInfo(uuid=ltask_uuid, **data)
        except (ValidationError, TypeError):
            raise LTaskInfo.InvalidFormat
