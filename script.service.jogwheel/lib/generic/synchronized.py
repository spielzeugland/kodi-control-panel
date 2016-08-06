from functools import wraps
from threading import RLock


def createLock(func):
    @wraps(func)
    def _wrapper(self, *args, **kwargs):
        self._synchronized_lock = RLock()
        return func(self, *args, **kwargs)
    return _wrapper


def withLock(func):
    @wraps(func)
    def _wrapper(self, *args, **kwargs):
        with self._synchronized_lock:
            return func(self, *args, **kwargs)
    return _wrapper
