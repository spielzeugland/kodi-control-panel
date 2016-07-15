from threading import Lock


_lock = Lock()
_unread = []
_archive = []
_archiveSize = 20


class _Message(object):
    def __init__(self, text, details, sysInfo):
        self.text = text
        self.details = details
        self.sysInfo = sysInfo
        self.time = None  # TODO add timestamp


def add(text, details=None, sysInfo=None):
    with _lock:
        global _unread
        global _archive
        global _archiveSize
        message = _Message(text, details, sysInfo)
        _unread.insert(0, message)
        _archive.insert(0, message)
        if len(_archive) > _archiveSize:
            _archive.pop()


def hasUnread():
    with _lock:
        global _unread
        return len(_unread) > 0


def getUnread():
    with _lock:
        global _unread
        temp = _unread
        _unread = []
        return temp


def archive():
    with _lock:
        global _archive
        return list(_archive)


def _clear():
    with _lock:
        global _unread
        global _archive
        _unread = []
        _archive = []
