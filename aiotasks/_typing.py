from typing import NewType, Union, List, Dict

LTaskUuid = NewType('LTaskUuid', str)
LTaskResult = Union[int, str, List, Dict]