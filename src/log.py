import logging


class _DefaultLogger(object):

    def __init__(self, name="Default", logger=logging.Logger):
        self._logger = logger(name)

    def error(self, msg, *args):
        self._logger.error(msg, *args)

    def warning(self, msg, *args):
        self._logger.warning(msg, *args)

    def info(self, msg, *args):
        self._logger.info(msg, *args)

    def debug(self, msg, *args):
        self._logger.debug(msg, *args)


_instance = None


def set(instance):
    global _instance
    _instance = instance


def useDefault():
    global _instance
    _instance = _DefaultLogger()


useDefault()


def error(msg, *args):
    _instance.error(msg, *args)


def warning(msg, *args):
    _instance.warning(msg, *args)


def info(msg, *args):
    _instance.info(msg, *args)


def debug(msg, *args):
    _instance.debug(msg, *args)
