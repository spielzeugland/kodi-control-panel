import sys
import threading
import messages

try:
    import queue
except ImportError:
    import Queue as queue


def createQueue():
    q = queue.Queue()
    q.worker = _Worker(q)
    return q


def asEvent(name, data=None):
    return {"name": name, "data": data}


class _Worker(threading.Thread):

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.daemon = True
        self._lock = threading.RLock()
        self._running = True
        self._queue = queue
        self._handler = None

    def run(self):
        while True:
            # TODO how to interrupt/stop thread while waiting here?
            event = self._queue.get()
            with self._lock:
                if not self._running:
                    return
            try:
                shouldContinue = self._handler(event)
                if shouldContinue is False:
                    return
            except Exception as e:
                text = "Error handling event \"{0}\"".format(event["name"])
                messages.add(text, None, sys.exc_info())
            with self._lock:
                if not self._running:
                    return

    def start(self, handler):
        if self._handler is None:
            self._handler = handler
        threading.Thread.start(self)

    def stop(self):
        with self._lock:
            self._running = False
