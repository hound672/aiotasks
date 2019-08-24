import random
import uuid

import pytest

from aiotasks._structs import LTaskInfo, LTaskStatus, LTaskException
from aiotasks._ltask import LTask

def get_ltask(*,
              res, exc):
    ltask = LTask(loop=None, ltask_manager=None, coro=None)
    ltask._res = res
    ltask._exc = exc
    return ltask

def test_from_ltask(faker):
    result = {faker.word(): faker.word()}
    ltask = get_ltask(res=result, exc=None)

    ltaskInfo: LTaskInfo = LTaskInfo.from_ltask(ltask_status=LTaskStatus.PROCESS, ltask=ltask)
    assert ltaskInfo.uuid == ltask.uuid
    assert ltaskInfo.result == result
    assert ltaskInfo.exc == None

def test_from_ltask_with_exception(faker):
    message = faker.word()
    exc = ValueError(message)
    ltask = get_ltask(res=None, exc=exc)

    ltaskInfo: LTaskInfo = LTaskInfo.from_ltask(ltask_status=LTaskStatus.PROCESS, ltask=ltask)

    assert ltaskInfo.uuid == ltask.uuid
    assert ltaskInfo.result == None
    assert ltaskInfo.exc.type == 'ValueError'
    assert ltaskInfo.exc.message == [message]


def test_from_ltask_with_invalid_exception(faker):
    ltask = get_ltask(res=None, exc=faker.word())

    ltaskInfo: LTaskInfo = LTaskInfo.from_ltask(ltask_status=LTaskStatus.PROCESS, ltask=ltask)

    assert ltaskInfo.uuid == ltask.uuid
    assert ltaskInfo.result == None
    assert ltaskInfo.exc == None

@pytest.mark.parametrize('uuid, status, result, exc', [
    ('uuid_1', LTaskStatus.PROCESS, None, None),
    ('uuid_2', LTaskStatus.PROCESS, {'r_key': 'v_key'}, None),
    ('uuid_3', LTaskStatus.PROCESS, None, LTaskException(type='ValueError', message=['err_message']))
])
def test_to_backend(uuid, status, result, exc):
    ltask_info = LTaskInfo(
        uuid=uuid,
        status=status,
        result=result,
        exc=exc
    )
    _uuid, data = ltask_info.to_backend()
    assert _uuid == uuid
    assert data['status'] == status.value
    assert data['result'] == result
    assert data['exc'] == None if exc is None else exc.__dict__

@pytest.mark.parametrize('uuid, status, result, exc', [
    ('uuid_1', LTaskStatus.PROCESS, None, None),
    ('uuid_2', LTaskStatus.SUCCESS, {'r_key': 'v_key'}, None),
    ('uuid_3', LTaskStatus.FAILURE, None, {'type': 'ValueError', 'message':['err_message']})
])
def test_from_backend(uuid, status, result, exc):
    data = {
        'status': status.value,
        'result': result,
        'exc': exc
    }
    ltask_info = LTaskInfo.from_backend(ltask_uuid=uuid, data=data)
    assert ltask_info.uuid == uuid
    assert ltask_info.status == status
    assert ltask_info.result == result
    _exc = None if exc is None else LTaskException(type=exc['type'], message=exc['message'])
    assert ltask_info.exc == _exc


def test_from_backend_invalid_empty_dict():
    data = {}
    _uuid = uuid.uuid4().hex
    with pytest.raises(LTaskInfo.InvalidFormat):
        LTaskInfo.from_backend(ltask_uuid=uuid, data=data)


def test_from_backend_invalid_data_not_dict(faker):
    data = faker.word()
    _uuid = uuid.uuid4().hex
    with pytest.raises(LTaskInfo.InvalidFormat):
        LTaskInfo.from_backend(ltask_uuid=_uuid, data=data)


def test_from_backend_invalid_exc_empty_dict(faker):
    data = {
        'status': LTaskStatus.FAILURE.value,
        'result': faker.word(),
        'exc': {}
    }
    _uuid = uuid.uuid4().hex
    with pytest.raises(LTaskInfo.InvalidFormat):
        LTaskInfo.from_backend(ltask_uuid=_uuid, data=data)


def test_from_backend_invalid_exc_not_dict(faker):
    data = {
        'status': LTaskStatus.FAILURE.value,
        'result': faker.word(),
        'exc': faker.word()
    }
    _uuid = uuid.uuid4().hex
    with pytest.raises(LTaskInfo.InvalidFormat):
        LTaskInfo.from_backend(ltask_uuid=_uuid, data=data)


def test_from_backend_invalid_wrong_status(faker):
    data = {
        'status': faker.word(),
        'result': faker.word(),
        'exc': None
    }
    _uuid = uuid.uuid4().hex
    with pytest.raises(LTaskInfo.InvalidFormat):
        LTaskInfo.from_backend(ltask_uuid=_uuid, data=data)


def test_from_backend_invalid_wrong_uuid(faker):
    data = {
        'status': LTaskStatus.FAILURE.value,
        'result': faker.word(),
        'exc': None
    }
    with pytest.raises(LTaskInfo.InvalidFormat):
        LTaskInfo.from_backend(ltask_uuid=[], data=data)
