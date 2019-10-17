# -*- coding: utf-8 -*-

"""

Brief description.

Some other description
"""

from abc import ABC, abstractmethod
from unittest import mock
from unittest.mock import create_autospec

import pytest

class ForTest(ABC):

    def for_test(self):
        return 'hello'

    @abstractmethod
    def abs(self):
        pass

    @abstractmethod
    def abs2(self):
        pass

def test_one():

    def tmp(self):
        return '123'

    # obj = ForTest()
    # with mock.patch(ForTest, abs=set()):

    with mock.patch.object(ForTest, '__abstractmethods__', None):
        with mock.patch.object(ForTest, 'abs', tmp):
            obj = ForTest()
            # breakpoint()
            pass

    # breakpoint()
    pass

class AsyncTest:
    async def method(self):
        return '123'

async def for_check(obj):
    res = await obj.method()
    pass
    return res

@pytest.mark.asyncio
async def test_async():
    # obj = create_autospec(AsyncTest)

    async def _mock_method(self):
        return '111'

    with mock.patch.object(AsyncTest, 'method', _mock_method):
        obj = AsyncTest()
        res = await for_check(obj)

    # obj.method.assert_awaited()

    assert res == '123'


