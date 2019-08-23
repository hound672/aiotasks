import random
import uuid
from unittest.mock import patch

import pytest

from aiotasks._backends._base import BaseBackend
from aiotasks._typing import LTaskUuid
from aiotasks._structs import LTaskInfo, LTaskStatus


class DummyBackend(BaseBackend):

    async def connect(self):
        pass

    async def _write(self, key: str, value: dict) -> None:
        pass


@pytest.fixture
def dummy_backend():
    return DummyBackend(loop=None, url=None)


def test_dump(event_loop, dummy_backend):
    ltask_info = LTaskInfo(uuid=LTaskUuid(uuid.uuid4().hex),
                           status=random.choice(list(LTaskStatus)))

    async def _fake(self, key: str, value: dict):
        assert key == ltask_info.uuid
        assert value == {'status': ltask_info.status.value}

    async def run():
        with patch.object(DummyBackend, '_write', new=_fake):
            await dummy_backend.write_task_info(ltask_info)

    event_loop.run_until_complete(run())
