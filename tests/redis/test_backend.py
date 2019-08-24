import pytest
import json
import uuid
import random

from aiotasks._exceptions import ErrorConnectBackend, LTaskNotFount
from aiotasks._backends._base import BaseBackend
from aiotasks._structs import LTaskStatus, LTaskInfo
from aiotasks._typing import LTaskUuid

def Ntest_error_connect(event_loop, redis_backend, faker):
    async def run():
        redis_backend._url = f'redis://{faker.ipv4_public()}:{faker.random_int()}/{faker.random_int()}'
        with pytest.raises(ErrorConnectBackend):
            await redis_backend.connect()

    event_loop.run_until_complete(run())

def test__write(event_loop, redis_backend, redis_client, faker):
    key = faker.word()
    value = {faker.word(): faker.word()}

    async def run():
        await redis_backend._write(key=key, value=value)
        read = await redis_client.get(key)
        assert read is not None
        assert json.loads(read) == value

    event_loop.run_until_complete(run())


def test__read(event_loop, redis_backend, redis_client, faker):
    key = faker.word()
    value = {faker.word(): faker.word()}

    async def run():
        await redis_client.set(key=key, value=json.dumps(value))
        read = await redis_backend._read(key=key)
        assert read == value

    event_loop.run_until_complete(run())


def test__read_invalid_data(event_loop, redis_backend, redis_client, faker):
    key = faker.word()

    async def run():
        await redis_client.set(key=key, value=faker.word())
        with pytest.raises(BaseBackend.RecordNotFound):
            await redis_backend._read(key=key)

    event_loop.run_until_complete(run())


def test__read_not_found(event_loop, redis_backend, faker):
    async def run():
        with pytest.raises(BaseBackend.RecordNotFound):
            await redis_backend._read(key=faker.word())

    event_loop.run_until_complete(run())


def test_write_task_info(event_loop, redis_backend, redis_client):
    ltask_info = LTaskInfo(uuid=LTaskUuid(uuid.uuid4().hex),
                           status=random.choice(list(LTaskStatus)))

    async def run():
        await redis_backend.write_task_info(ltask_info)
        read = await redis_client.get(BaseBackend._get_task_key(ltask_info.uuid))
        assert read is not None
        assert json.loads(read) == {
            'status': ltask_info.status.value,
            'result': None,
            'exc': None
        }

    event_loop.run_until_complete(run())


def test_read_task_info(event_loop, redis_backend, redis_client):
    ltask_info = LTaskInfo(uuid=LTaskUuid(uuid.uuid4().hex),
                           status=random.choice(list(LTaskStatus)))

    async def run():
        data = {
            'status': ltask_info.status.value,
            'result': None,
            'exc': None
        }
        await redis_client.set(key=BaseBackend._get_task_key(ltask_info.uuid), value=json.dumps(data))
        ltask_read = await redis_backend.read_task_info(ltask_uuid=ltask_info.uuid)
        assert ltask_read == ltask_info

    event_loop.run_until_complete(run())


def test_read_task_info_not_found(event_loop, redis_backend, redis_client):
    async def run():
        with pytest.raises(LTaskNotFount):
            await redis_backend.read_task_info(ltask_uuid=uuid.uuid4().hex)

    event_loop.run_until_complete(run())


def test_read_task_info_invalid_data(event_loop, redis_backend, redis_client, faker):
    key = uuid.uuid4().hex
    async def run():
        await redis_client.set(key=key, value=faker.word())
        with pytest.raises(LTaskNotFount):
            await redis_backend.read_task_info(ltask_uuid=key)

    event_loop.run_until_complete(run())
