import time
import context
import mocks
from util import Timer


def someCallback():
    pass


def test_construtorWithOptionalTimeout():
    c = Timer(someCallback)
    assert c._timeout == 5


def test_initial_shouldBeNotRunning():
    c = Timer(someCallback, 1)
    assert c.isNotRunning() is True
    assert c.isRunning() is False


def test_start_shouldStartTimer():
    c = Timer(someCallback, 1)
    c.start()
    assert c.isNotRunning() is False
    assert c.isRunning() is True


def test_start_shouldReturnFalse_whenTimerWasNotRunningBefore():
    c = Timer(someCallback, 1)
    assert c.start() is False


def test_start_shouldReturnTrue_whenTimerWasInRunningModeBefore():
    c = Timer(someCallback, 1)
    c.start()
    assert c.start() is True


def test_shouldBeStoppedAfterTimeout():
    counter = mocks.CountingMethod()
    c = Timer(counter.get(), 0.2)
    c.start()
    assert c.isRunning() is True
    time.sleep(0.5)
    assert c.isNotRunning() is True
    assert counter.count == 1


def test_start_shouldExtendTimer():
    c = Timer(someCallback, 0.5)
    c.start()
    assert c.isNotRunning() is False
    time.sleep(0.3)
    c.start()
    assert c.isNotRunning() is False
    c.start()
    time.sleep(0.3)
    assert c.isNotRunning() is False
    c.start()
    time.sleep(0.7)
    assert c.isNotRunning() is True


def test_cancel_shouldStopTimer():
    counter = mocks.CountingMethod()
    c = Timer(counter.get(), 1)
    c.start()
    c.cancel()
    assert c. isNotRunning() is True
    assert counter.count == 0


def test_cancel_shouldDoNothingWhenNotRunning():
    c = Timer(someCallback, 1)
    c.cancel()
    assert c. isNotRunning() is True
