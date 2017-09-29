import context
import mocks
import menu
from kodiMenu import *


def test_ShutdownAction_shouldBeSubClassOfAction():
    assert isinstance(ShutdownAction(None), menu.Action)


def test_ShutdownAction_init_shouldTakeName():
    action = ShutdownAction(None, "myName")
    assert action.name() == "myName"


def test_ShutdownAction_init_shouldUseDefaultName():
    assert ShutdownAction(None).name() == "Shutdown"


def test_ShutdownAction_run_shouldDelegateToKodi():
    kodi = mocks.kodi.Kodi()
    ShutdownAction(kodi).run(None)
    assert kodi.shutdownCnt == 1


def test_RebootAction_shouldBeSubClassOfAction():
    assert isinstance(RebootAction(None), menu.Action)


def test_RebootAction_init_shouldTakeName():
    action = RebootAction(None, "myName")
    assert action.name() == "myName"


def test_RebootAction_init_shouldUseDefaultName():
    assert RebootAction(None).name() == "Reboot"


def test_RebootAction_run_shouldDelegateToKodi():
    kodi = mocks.kodi.Kodi()
    RebootAction(kodi).run(None)
    assert kodi.rebootCnt == 1
