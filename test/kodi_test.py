import context
import mocks
from kodi import Kodi


def test_shouldHaveConstructor():
    xbmc = mocks.Xbmc()
    proxy = mocks.Proxy()
    Kodi(proxy, xbmc)


def test_getMonitor_isAbortRequested_shouldReturnFalse():
    xbmc = mocks.Xbmc()
    proxy = mocks.Proxy()
    kodi = Kodi(proxy, xbmc)
    assert kodi.getMonitor().abortRequested() is False


def test_getMonitor_isAbortRequested_shouldReturnTrue():
    xbmc = mocks.Xbmc()
    proxy = mocks.Proxy()
    kodi = Kodi(proxy, xbmc)
    mocks.Xbmc.abortRequested = True
    assert kodi.getMonitor().abortRequested() is True


def test_withoutXbmc_getMonitor_isAbortRequested_shouldReturnFalse():
    proxy = mocks.Proxy()
    kodi = Kodi(proxy, None)
    assert kodi.getMonitor().abortRequested() is False


def test_withoutXbmc_getMonitor_isAbortRequested_shouldReturnFalse():
    proxy = mocks.Proxy()
    kodi = Kodi(proxy, None)
    assert kodi.getMonitor().abortRequested() is False


def test_withoutXbmc_getMonitor_waitForAbort_shouldDoNothing():
    proxy = mocks.Proxy()
    kodi = Kodi(proxy, None)
    kodi.getMonitor().waitForAbort(1)
