import time
from worker import run, runAsLoop, _Worker
import mocks


def test_init():
    _Worker(mocks.CountingMethod().get())


def test_run():
    counter = mocks.CountingMethod()
    worker = run(counter.get())
    worker.join()
    assert counter.count == 1


def test_runAsLoop():
    counter = mocks.CountingMethod()
    worker = runAsLoop(counter.get())
    time.sleep(0.2)  # might be shaky
    worker.stop()
    assert counter.count > 1


def test_stop_runningAsLoop():
    counter = mocks.CountingMethod(mocks.returnFalse)
    worker = runAsLoop(counter.get())
    worker.join()
    assert counter.count == 1
