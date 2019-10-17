# -*- coding: utf-8 -*-

"""

Brief description.

Some other description
"""

from unittest.mock import patch

class SomeClass:
    def logic(self, value, val):
        # read from socker, for instance
        return value + '_HELLO'

    def process(self, value):
        return self.logic(value)


def test_one():

    with patch.object(SomeClass, 'logic', return_value='DATA', autospec=True) as _mock:
        obj = SomeClass()
        res = obj.process('HELLO')
        breakpoint()

        # _mock.assert_called()
        _mock.assert_called_with(obj, 'HELLO')
