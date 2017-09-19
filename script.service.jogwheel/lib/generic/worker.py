import sys
import threading
import messages

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

    def __init__(self, handler, loop=False):
        threading.Thread.__init__(self)
        self.daemon = True
        self._lock = threading.RLock()
        self._shouldStop = False
        self._handler = handler
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
                return self._handler()
            except Exception as e:
                text = "Error handling event \"{0}\"".format(event["name"])
                # switch to logging here
                messages.add(text, None, sys.exc_info())

    def stop(self):
        with self._lock:
            self._shouldStop = False

    def shouldStop(self):
        with self._lock:
            return self._shouldStop
