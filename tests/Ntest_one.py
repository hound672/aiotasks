# -*- coding: utf-8 -*-

"""

Brief description.

Some other description
"""

from abc import ABC, abstractmethod
from unittest import mock
from unittest.mock import create_autospec, AsyncMock


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
        return '123'

    with mock.patch.object(AsyncTest, 'method', _mock_method):
        obj = AsyncTest()
        res = await for_check(obj)

    # obj.method.assert_awaited()

    assert res == '123'


@pytest.mark.asyncio
async def test_async2():
    obj = create_autospec(AsyncTest)

    obj.method.return_value = '111'

    res = await for_check(obj)
    assert res == '111'
    obj.method.assert_awaited()



class NewClass:

    async def async_proc(self):
        return await self.async_func('111')

    async def async_func(self, val, val2):
        return '123' + val

    def sync_func(self, val):
        return '456'


async def _async_side(self, val):
    return '!!!' + val

def _sync_side(self, val):
    return 'SYNC' + val

@pytest.mark.asyncio
async def Ntest_again():

    with mock.patch.object(NewClass, 'async_func', _async_side):
        obj = NewClass()
        res1 = await obj.async_func('123')

        res_tmp1 = await obj.async_proc()

    with mock.patch.object(NewClass, 'sync_func', _sync_side):
        obj = NewClass()
        res2 = obj.sync_func('123')

    # breakpoint()
    pass


@pytest.mark.asyncio
async def test_over():
    obj = NewClass()
    obj.async_func = AsyncMock(spec=NewClass.async_func, return_value='000')

    res = await obj.async_proc()


    # breakpoint()
    pass


class Target:
    async def apply(self, sure):
        return sure

async def method(target, value):
    return await target.apply(value)

@pytest.mark.asyncio
async def Ntest_over1():
    obj_mock = create_autospec(Target)
    await method(obj_mock, 'value')
    obj_mock.apply.assert_awaited_with('value')


@pytest.mark.asyncio
async def test_over2():

    target = Target()

    # target.apply = AsyncMock()
    target.apply = AsyncMock(spec=target.apply)
    # target.apply = AsyncMock(autospec=True)

    # await method(target, "value")
    await target.apply('value')

    target.apply.assert_awaited_with("value")


@pytest.mark.asyncio
async def Ntest_over3():
    with mock.patch.object(Target, 'apply', return_value='222', autospec=True) as _mock:
    # with mock.patch.object(Target, 'apply', return_value='222') as _mock:

        obj = Target()


        res = await obj.apply('val')
        # breakpoint()
        #
        # assert _mock == obj.apply
        # _mock.assert_awaited_with(obj, 'val')
        #
        #
        # pass

