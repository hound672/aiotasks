from ._base import BaseBackend

class DummyBackend(BaseBackend):

    async def connect(self) -> None:
        pass  # pragma: no cover

    async def close(self) -> None:
        pass  # pragma: no cover

    async def _write(self, key: str, data: dict) -> None:
        pass  # pragma: no cover

    async def _read(self, key: str) -> dict:
        pass  # pragma: no cover
