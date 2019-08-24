from typing import Type

from ._exceptions import UnknownBackend
from ._backends._base import BaseBackend
from ._backends._dummy import DummyBackend
from ._backends._redis import RedisBackend
# TODO import from list of string like in Celery backend loader

def get_backend_by_url(url: str) -> Type[BaseBackend]:
    """Return backend by its url"""
    backends = {
        'dummy': DummyBackend,
        'redis': RedisBackend
    }

    schema, _, _ = url.partition('://')
    try:
        backend = backends[schema]
        return backend
    except KeyError:
        raise UnknownBackend
