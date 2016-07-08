import context
from threading import Thread
from time import sleep
from synchronized import withLock, createLock


class SomeClass():

    @createLock
    def __init__(self, name="someName"):
        self._name = name
        self._waiting = True
        self.checkWaitingWasCalled = False

    @withLock
    def greet(self):
        return "hello " + self._name

    @withLock
    def wait(self):
        while self._waiting:
            pass

    @withLock
    def checkWaiting(self):
        self.checkWaitingWasCalled = True

    def stopWaiting(self):
        self._waiting = False


def test_decorateMethod_shouldPassValues():
    assert SomeClass("world").greet() == "hello world"


def test_decoratedMethod_hasCorrectAttributes():
    assert SomeClass("").greet.__name__ == "greet"


def test_decoratedMethod_shouldUseLock():
    o = SomeClass()

    runningThread = Thread(target=o.wait)
    runningThread.setDaemon(True)
    runningThread.start()

    blockingThread = Thread(target=o.checkWaiting)
    blockingThread.setDaemon(True)
    blockingThread.start()

    assert o.checkWaitingWasCalled is False

    o.stopWaiting()

    sleep(0.1)

    assert o.checkWaitingWasCalled is True
