from time import sleep
import context
import mocks
from menu import AsyncAction, Action


someMenu = None


class AsyncActionForTest(AsyncAction):

    def __init__(self, name, delay=0):
        super(AsyncActionForTest, self).__init__(name)
        self._delay = delay
        self.runCnt = 0

    def _asyncRun(self):
        sleep(self._delay)
        self.runCnt += 1


def test_shouldBeSubClassOfFolder():
    assert isinstance(AsyncAction(""), Action)


def test_name_shouldReturnName():
    action = AsyncAction("myName")
    assert action.name() == "myName"


def test_run_shouldBeAsynchron():
    action = AsyncActionForTest("name", 0.1)
    action.run(someMenu)
    assert action.runCnt == 0
    sleep(0.2)
    assert action.runCnt == 1


def test_run_shouldNotRunIfCurrentlyRunning():
    action = AsyncActionForTest("name", 0.1)
    action.run(someMenu)
    action.run(someMenu)
    sleep(0.2)
    assert action.runCnt == 1
