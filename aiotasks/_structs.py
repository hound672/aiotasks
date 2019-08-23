from dataclasses import dataclass
from enum import Enum, auto

from ._typing import LTaskUuid


class LTaskStatus(Enum):
    def _generate_next_value_(name, start, count, last_values):  # type: ignore
        return name

    NOT_FOUND = auto()
    PROCESS = auto()
    DONE = auto()

@dataclass
class LTaskInfo:
    uuid: LTaskUuid
    status: LTaskStatus
