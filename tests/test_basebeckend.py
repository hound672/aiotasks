import random
import uuid
from unittest.mock import patch

import pytest

from aiotasks._backends._base import BaseBackend
from aiotasks._typing import LTaskUuid
from aiotasks._structs import LTaskInfo, LTaskStatus, LTaskException
from aiotasks._exceptions import LTaskNotFount


class DummyBackend(BaseBackend):

    async def connect(self):
        pass

    async def close(self) -> None:
        pass

    async def _write(self, key: str, data: dict) -> None:
        pass

    async def _read(self, key: str) -> dict:
        pass


@pytest.fixture
def dummy_backend():
    return DummyBackend(loop=None, url=None)


def test__get_task_key(dummy_backend):
    ltask_uuid = LTaskUuid(uuid.uuid4().hex)
    assert dummy_backend._get_task_key(ltask_uuid) == f'aiotasks-task-{ltask_uuid}'


def test__write_called(event_loop, dummy_backend):
    ltask_info = LTaskInfo(
        uuid=uuid.uuid4().hex,
        status=LTaskStatus.SUCCESS
    )

    async def _fake(self, key: str, data: dict):
        globals()['write_called'] = True

    async def run():
        with patch.object(DummyBackend, '_write', new=_fake):
            await dummy_backend.write_task_info(ltask_info)

    event_loop.run_until_complete(run())
    assert globals()['write_called']


@pytest.mark.parametrize('uuid, status, result, exc', [
    ('uuid_1', LTaskStatus.PROCESS, None, None),
    ('uuid_2', LTaskStatus.PROCESS, {'r_key': 'v_key'}, None),
    ('uuid_3', LTaskStatus.PROCESS, None, LTaskException(type='ValueError', message=['err_message']))
])
def test_write_task_info(uuid, status, result, exc, event_loop, dummy_backend):
    ltask_info = LTaskInfo(
        uuid=uuid,
        status=status,
        result=result,
        exc=exc
    )

    async def _fake(self, key: str, data: dict):
        assert key == dummy_backend._get_task_key(uuid)
        assert data == {'status': status.value, 'result': result, 'exc': None if exc is None else exc.__dict__}

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
                await dummy_backend.read_task_info(uuid.uuid4().hex)

    event_loop.run_until_complete(run())


@pytest.mark.parametrize('uuid, status, result, exc', [
    ('uuid_1', LTaskStatus.PROCESS, None, None),
    ('uuid_2', LTaskStatus.SUCCESS, {'r_key': 'v_key'}, None),
    ('uuid_3', LTaskStatus.FAILURE, None, {'type': 'ValueError', 'message':['err_message']})
])
def test_read_task_info(uuid, status, result, exc, event_loop, dummy_backend):
    data = {
        'status': status.value,
        'result': result,
        'exc': exc
    }

    async def _fake(self, key: str):
        assert key == dummy_backend._get_task_key(uuid)
        return {'status': status.value, 'result': result, 'exc': exc}

    async def run():
        with patch.object(DummyBackend, '_read', new=_fake):
            ltask_info = await dummy_backend.read_task_info(uuid)
            assert ltask_info == LTaskInfo.from_backend(ltask_uuid=uuid, data=data)

    event_loop.run_until_complete(run())
