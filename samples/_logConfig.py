import logging
import configuredLogging


def configure(debug=False):
    level = logging.WARNING
    if debug:
        level = logging.DEBUG
    msgFormat = configuredLogging.FORMAT
    dateFormat = configuredLogging.DATE_FORMAT
    logging.basicConfig(level=level, format=msgFormat, datefmt=dateFormat)
    configuredLogging.configure(level)
