import sys
import threading
import configuredLogging as logging

try:
    import queue
except ImportError:
    import Queue as queue


def createQueue():
    return queue.Queue()


def run(workload):
    worker = _Worker(workload)
    worker.start()
    return worker


def runAsLoop(workload):
    worker = _Worker(workload, True)
    worker.start()
    return worker


class _Worker(threading.Thread):

    def __init__(self, task, loop=False):
        threading.Thread.__init__(self)
        self.daemon = True
        self._lock = threading.RLock()
        self._shouldStop = False
        self._task = task
        self._loop = loop

    def run(self):
        if self._loop is False:
            self._runInternal()
        else:
            while True:
                if self.shouldStop():
                    return
                shouldContinue = self._runInternal()
                if shouldContinue is False:
                    return

    def _runInternal(self):
            try:
                return self._task()
            except Exception as e:
                text = "Error handling event"
                logging.exception(text)

    def stop(self):
        with self._lock:
            self._shouldStop = False

    def shouldStop(self):
        with self._lock:
            return self._shouldStop
