from threading import Timer
from synchronized import createLock, withLock


# TODO find a better name
class ExtensibleTimer(object):

    @createLock
    def __init__(self, task, timeout=5):
        self._timer = None
        self._timeout = timeout
        self._task = task

    @withLock
    def start(self):
        if self._timer is None:
            self._timer = self._createAndStartTimer()
            return False
        else:
            self._timer.cancel()
            self._timer = self._createAndStartTimer()
            return True

    @withLock
    def _createAndStartTimer(self):
        timer = Timer(self._timeout, self._handleTimeout)
        timer.setDaemon(True)
        timer.start()
        return timer

    def _handleTimeout(self):
        self.cancel()
        self._task()

    @withLock
    def cancel(self):
        if self._timer is not None:
            self._timer.cancel()
            self._timer = None

    @withLock
    def isRunning(self):
        return self._timer is not None

    @withLock
    def isNotRunning(self):
        return self._timer is None
