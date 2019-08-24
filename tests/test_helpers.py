import pytest

from aiotasks._exceptions import UnknownBackend
from aiotasks._backends._redis import RedisBackend
from aiotasks._backends._dummy import DummyBackend
from aiotasks._helpers import get_backend_by_url


def test_get_dummy_backend():
    url = 'dummy://host:port'
    backend = get_backend_by_url(url)
    assert backend == DummyBackend


def test_get_redis_backend():
    url = 'redis://host:port'
    backend = get_backend_by_url(url)
    assert backend == RedisBackend

def test_unkownn_backend(faker):
    url = f'faker.word()://host:port'
    with pytest.raises(UnknownBackend):
        get_backend_by_url(url)


def test_empty_url():
    url = f''
    with pytest.raises(UnknownBackend):
        get_backend_by_url(url)


def test_empty_schema():
    url = f'://host:port'
    with pytest.raises(UnknownBackend):
        get_backend_by_url(url)
