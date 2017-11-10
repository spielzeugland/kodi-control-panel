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


def error(msg, *args, **kwargs):
    _rootLogger.error(msg, *args, **kwargs)


def warning(msg, *args, **kwargs):
    _rootLogger.warning(msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    _rootLogger.info(msg, *args, **kwargs)


def debug(msg, *args, **kwargs):
    _rootLogger.debug(msg, *args, **kwargs)


def exception(msg=None, *args, **kwargs):
    _rootLogger.exception(msg, *args, **kwargs)


DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL
