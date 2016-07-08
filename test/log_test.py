import context
import mocks
from functools import wraps
import log
from log import _DefaultLogger


def after(func):
    @wraps(func)
    def _wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        finally:
            log.useDefault()
    return _wrapper


def assertMessage(logging, level, message, arg1, arg2):
    assert logging.recorded[level]["message"] == message
    assert logging.recorded[level]["args"][0] == arg1
    assert logging.recorded[level]["args"][1] == arg2


def test_defaultLoggerShouldBeSetInitialially():
    assert isinstance(log._instance, log._DefaultLogger)


@after
def test_log_setShouldChangeLogInstance():
    o = object()
    log.set(o)
    assert log._instance is o


@after
def test_DefaultLogger_init_shouldCreateLoggerWithName():
    logging = mocks.logging()
    _DefaultLogger("myName", logging.logger)
    assert logging.name == "myName"


@after
def test_DefaultLoger_error():
    logging = mocks.logging()
    logger = _DefaultLogger("myName", logging.logger)
    message = "Message"
    arg1 = object()
    arg2 = 42
    logger.error(message, arg1, arg2)
    assertMessage(logging, "error", message, arg1, arg2)


@after
def test_error():
    logging = mocks.logging()
    logger = _DefaultLogger("myName", logging.logger)
    log.set(logger)

    message = "Message"
    arg1 = object()
    arg2 = 42
    log.error(message, arg1, arg2)
    assertMessage(logging, "error", message, arg1, arg2)


@after
def test_DefaultLogger_warning():
    logging = mocks.logging()
    logger = _DefaultLogger("myName", logging.logger)
    message = "Message"
    arg1 = object()
    arg2 = 42
    logger.warning(message, arg1, arg2)
    assertMessage(logging, "warning", message, arg1, arg2)


@after
def test_warning():
    logging = mocks.logging()
    logger = _DefaultLogger("myName", logging.logger)
    log.set(logger)

    message = "Message"
    arg1 = object()
    arg2 = 42
    log.warning(message, arg1, arg2)
    assertMessage(logging, "warning", message, arg1, arg2)


@after
def test_DefaultLogger_info():
    logging = mocks.logging()
    logger = _DefaultLogger("myName", logging.logger)
    message = "Message"
    arg1 = object()
    arg2 = 42
    logger.info(message, arg1, arg2)
    assertMessage(logging, "info", message, arg1, arg2)


@after
def test_info():
    logging = mocks.logging()
    logger = _DefaultLogger("myName", logging.logger)
    log.set(logger)

    message = "Message"
    arg1 = object()
    arg2 = 42
    log.info(message, arg1, arg2)
    assertMessage(logging, "info", message, arg1, arg2)


@after
def test_DefaultLogger_debug():
    logging = mocks.logging()
    logger = _DefaultLogger("myName", logging.logger)
    message = "Message"
    arg1 = object()
    arg2 = 42
    logger.debug(message, arg1, arg2)
    assertMessage(logging, "debug", message, arg1, arg2)


@after
def test_debug():
    logging = mocks.logging()
    logger = _DefaultLogger("myName", logging.logger)
    log.set(logger)

    message = "Message"
    arg1 = object()
    arg2 = 42
    log.debug(message, arg1, arg2)
    assertMessage(logging, "debug", message, arg1, arg2)
