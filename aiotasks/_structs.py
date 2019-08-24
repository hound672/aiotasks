from dataclasses import dataclass
from enum import Enum, auto
from typing import Union, Dict, Optional, List

from ._typing import LTaskUuid, LTaskResult


class LTaskStatus(Enum):
    def _generate_next_value_(name, start, count, last_values):  # type: ignore
        return name

    PROCESS = auto()
    SUCCESS = auto()
    FAILURE = auto()

@dataclass
class LTaskException:
    type: str
    message: List


@dataclass
class LTaskInfo:
    uuid: LTaskUuid
    status: LTaskStatus
    result: Optional[LTaskResult] = None
    exc: Optional[LTaskException] = None
