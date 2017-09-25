import logging
try:
    from logging import NullHandler  # NullHandler was introduced with 2.7
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass


# TODO find a good name
__ROOT = "jogwheel"
__PATTERN = __ROOT + ".{0}"
FORMAT = '%(asctime)s - %(levelname)s - %(name)s:%(lineno)d %(message)s'
DATE_FORMAT = '%d.%m.%Y %H:%M:%S'


_rootLogger = logging.getLogger(__ROOT)
_rootLogger.addHandler(NullHandler())


def getLogger(name):
    fullName = __PATTERN.format(name)
    return logging.getLogger(fullName)
    # TODO use if exists
    # return _rootLogger.getChild(name)


def configure(level, handler=None):
    _rootLogger.setLevel(level)
    if handler is not None:
        _rootLogger.addHandler(handler)


def error(msg, *args):
    _rootLogger.error(msg, *args)


def warning(msg, *args):
    _rootLogger.warning(msg, *args)


def info(msg, *args):
    _rootLogger.info(msg, *args)


def debug(msg, *args):
    _rootLogger.debug(msg, *args)


DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL
