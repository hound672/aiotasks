import random
import uuid
from unittest.mock import patch

import pytest

from aiotasks._backends._base import BaseBackend
from aiotasks._typing import LTaskUuid
from aiotasks._structs import LTaskInfo, LTaskStatus
from aiotasks._exceptions import LTaskNotFount


class DummyBackend(BaseBackend):

    async def connect(self):
        pass

    async def close(self) -> None:
        pass

    async def _write(self, key: str, value: dict) -> None:
        pass

    async def _read(self, key: str) -> dict:
        pass


@pytest.fixture
def dummy_backend():
    return DummyBackend(loop=None, url=None)


def test_write_task_info(event_loop, dummy_backend):
    ltask_info = LTaskInfo(uuid=LTaskUuid(uuid.uuid4().hex),
                           status=random.choice(list(LTaskStatus)))

    async def _fake(self, key: str, value: dict):
        assert key == f'aiotasks-task-{ltask_info.uuid}'
        assert value == {'status': ltask_info.status.value}

    async def run():
        with patch.object(DummyBackend, '_write', new=_fake):
            await dummy_backend.write_task_info(ltask_info)

    event_loop.run_until_complete(run())

def test_read_task_info_record_not_found(event_loop, dummy_backend):
    async def _fake(self, key: str):
        raise BaseBackend.RecordNotFound

    async def run():
        with patch.object(DummyBackend, '_read', new=_fake):
            with pytest.raises(LTaskNotFount):
                await dummy_backend.read_task_info(ltask_uuid=uuid.uuid4().hex)

    event_loop.run_until_complete(run())


def test_read_task_info_record_invalid_status(event_loop, dummy_backend, faker):
    async def _fake(self, key: str):
        return {'status': faker.word()}

    async def run():
        with patch.object(DummyBackend, '_read', new=_fake):
            with pytest.raises(LTaskNotFount):
                await dummy_backend.read_task_info(ltask_uuid=uuid.uuid4().hex)

    event_loop.run_until_complete(run())


def test_read_task_info_record_invalid_struct_data(event_loop, dummy_backend, faker):
    async def _fake(self, key: str):
        return {faker.word(): faker.word()}

    async def run():
        with patch.object(DummyBackend, '_read', new=_fake):
            with pytest.raises(LTaskNotFount):
                await dummy_backend.read_task_info(ltask_uuid=uuid.uuid4().hex)

    event_loop.run_until_complete(run())


def test_read_task_info_record_invalid_data(event_loop, dummy_backend, faker):
    async def _fake(self, key: str):
        return faker.word()

    async def run():
        with patch.object(DummyBackend, '_read', new=_fake):
            with pytest.raises(LTaskNotFount):
                await dummy_backend.read_task_info(ltask_uuid=uuid.uuid4().hex)

    event_loop.run_until_complete(run())


def test_read_task_info_record(event_loop, dummy_backend):
    ltask_info = LTaskInfo(uuid=LTaskUuid(uuid.uuid4().hex),
                           status=random.choice(list(LTaskStatus)))

    async def _fake(self, key: str):
        assert key == f'aiotasks-task-{ltask_info.uuid}'
        return {'status': ltask_info.status.value}

    async def run():
        with patch.object(DummyBackend, '_read', new=_fake):
            _ltask_info = await dummy_backend.read_task_info(ltask_uuid=ltask_info.uuid)
            assert ltask_info == _ltask_info

    event_loop.run_until_complete(run())
