import logging
import configuredLogging


class SimpleLogHandler(logging.Handler):

    def __init__(self):
        super(SimpleLogHandler, self).__init__()
        msgFormat = '%(name)s:%(lineno)d: %(message)s'
        formatter = logging.Formatter(fmt=msgFormat)
        self.setFormatter(formatter)

    def emit(self, record):
        msg = self.format(record)
        print(msg)


def configure(debug=False):
    level = logging.WARNING
    if debug:
        level = logging.DEBUG
    msgFormat = configuredLogging.FORMAT
    dateFormat = configuredLogging.DATE_FORMAT
    logging.basicConfig(level=level, format=msgFormat, datefmt=dateFormat)
    configuredLogging.configure(level)
