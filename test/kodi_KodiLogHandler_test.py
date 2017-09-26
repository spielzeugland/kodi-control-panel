import context
import mocks
import kodi
import logging


def _assertMessage(xbmc, msg, level):
    assert len(xbmc.messages) == 1
    assert xbmc.messages[0]["msg"] == msg
    assert xbmc.messages[0]["level"] == level


def test_constructor():
    kodi.KodiLogHandler(None)


def test_emit_info():
    xbmc = mocks.Xbmc()
    record = logging.LogRecord("myName", logging.INFO, "myPathName", 12345, "myMsg", None, None)
    handler = kodi.KodiLogHandler(xbmc)
    handler.emit(record)
    _assertMessage(xbmc, "myName:12345: myMsg", xbmc.LOGNOTICE)


def test_emit_debug():
    xbmc = mocks.Xbmc()
    record = logging.LogRecord("myName", logging.DEBUG, "myPathName", 12345, "myMsg", None, None)
    handler = kodi.KodiLogHandler(xbmc)
    handler.emit(record)
    _assertMessage(xbmc, "myName:12345: myMsg", xbmc.LOGDEBUG)


def _convertAndAssertLevel(pythonLevel, expectedXbmcLevel):
    xbmc = mocks.Xbmc()
    handler = kodi.KodiLogHandler(xbmc)
    xbmcLevel = handler._convertLevel(pythonLevel)
    assert xbmcLevel == expectedXbmcLevel


def test_convertLevel_critical():
    _convertAndAssertLevel(logging.CRITICAL, mocks.Xbmc.LOGFATAL)


def test_convertLevel_critical_1more():
    _convertAndAssertLevel(logging.CRITICAL + 1, mocks.Xbmc.LOGFATAL)


def test_convertLevel_critical_1less():
    _convertAndAssertLevel(logging.CRITICAL - 1, mocks.Xbmc.LOGERROR)


def test_convertLevel_error():
    _convertAndAssertLevel(logging.ERROR, mocks.Xbmc.LOGERROR)


def test_convertLevel_error_1more():
    _convertAndAssertLevel(logging.ERROR + 1, mocks.Xbmc.LOGERROR)


def test_convertLevel_error_1less():
    _convertAndAssertLevel(logging.ERROR - 1, mocks.Xbmc.LOGWARNING)


def test_convertLevel_warning():
    _convertAndAssertLevel(logging.WARNING, mocks.Xbmc.LOGWARNING)


def test_convertLevel_warning_1more():
    _convertAndAssertLevel(logging.WARNING + 1, mocks.Xbmc.LOGWARNING)


def test_convertLevel_warning_1less():
    _convertAndAssertLevel(logging.WARNING - 1, mocks.Xbmc.LOGNOTICE)


def test_convertLevel_info():
    _convertAndAssertLevel(logging.INFO, mocks.Xbmc.LOGNOTICE)


def test_convertLevel_info_1more():
    _convertAndAssertLevel(logging.INFO + 1, mocks.Xbmc.LOGNOTICE)


def test_convertLevel_info_1less():
    _convertAndAssertLevel(logging.INFO - 1, mocks.Xbmc.LOGDEBUG)


def test_convertLevel_debug():
    _convertAndAssertLevel(logging.DEBUG, mocks.Xbmc.LOGDEBUG)


def test_convertLevel_debug_1more():
    _convertAndAssertLevel(logging.DEBUG + 1, mocks.Xbmc.LOGDEBUG)


def test_convertLevel_debug_1less():
    _convertAndAssertLevel(logging.DEBUG - 1, mocks.Xbmc.LOGDEBUG)
