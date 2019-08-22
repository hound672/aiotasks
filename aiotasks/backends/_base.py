from abc import ABC


class BaseBackend(ABC):
    """Base class for Backend"""

    async def get(self):
        pass
