from unittest.mock import MagicMock, patch


def executor():
    return 'NOT_MOCKED'

def process():
    res = executor()
    return res

def side():
    return 'SIDE EFFECT'


def test_three_one():

    with patch('test_three.executor', side_effect=executor) as _mock:
        res = process()
        # breakpoint()
        pass


class ForTest:
    def executor(self):
        breakpoint()
        return 'NOT_MOCKED'

    def process(self):
        res = self.executor()
        return res

def test_three_two():

    obj = ForTest()

    with patch.object(ForTest, 'executor', side_effect=ForTest.executor, autospec=True) as _mock:
        res = obj.process()
        breakpoint()
        pass


