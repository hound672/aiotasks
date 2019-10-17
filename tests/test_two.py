# -*- coding: utf-8 -*-

"""

Brief description.

Some other description
"""

from unittest.mock import patch, MagicMock, Mock

class SomeClass:
    def logic(self, value):
        # read from socker, for instance
        return value + '_HELLO'

    def process(self, value):
        return self.logic(value)


def Ntest_one():

    # with patch.object(SomeClass, 'logic', return_value='DATA', autospec=True) as _mock:
    with patch.object(SomeClass, 'logic', autospec=True) as _mock:
        obj = SomeClass()
        res = obj.process('HELLO')
        breakpoint()

        # _mock.assert_called()
        _mock.assert_called_with('HELLO')


@patch.object(SomeClass, 'logic', autospec=True)
def test_two(_mock):
    obj = SomeClass()
    res = obj.process('HELLO')

    _mock.assert_called()
    # _mock.assert_called_with('HELLO')


def Ntest_three():
    obj = SomeClass()

    obj.logic = Mock(spec=obj.logic)
    obj.logic.return_value = 'DATA'

    res = obj.process('HELLO')

    breakpoint()

    # obj.logic.assert_called_with('HELLO')
