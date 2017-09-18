import time
import context
import mocks
from controller import Controller, _ModeTimer as ModeTimer


someController = Controller(None, mocks.Menu())


def test_construtorWithOptionalTimeout():
    c = ModeTimer(someController)
    assert c._timeout == 5


def test_initial_shouldBeMainMode():
    c = ModeTimer(someController, 1)
    assert c.isMainMode() is True


def test_mainMode_updateShouldEnableMenuMode():
    c = ModeTimer(someController, 1)
    c.update()
    assert c.isMainMode() is False


def test_mainMode_updateShouldReturnFalse():
    c = ModeTimer(someController, 1)
    assert c.update() is False


def test_menuMode_updateShouldReturnTrue():
    c = ModeTimer(someController, 1)
    c.update()
    assert c.update() is True


def test_menuMode_shouldBeExitedAfterTimeout():
    c = ModeTimer(someController, 0.2)
    c.update()
    assert c.isMainMode() is False
    time.sleep(0.5)
    assert c.isMainMode() is True


def test_menuMode_updateShouldBeExtendMenuMode():
    c = ModeTimer(someController, 0.5)
    c.update()
    assert c.isMainMode() is False
    time.sleep(0.3)
    c.update()
    assert c.isMainMode() is False
    c.update()
    time.sleep(0.3)
    assert c.isMainMode() is False
    c.update()
    time.sleep(0.7)
    assert c.isMainMode() is True


def test_menuMode_cancelShouldExitMenuMode():
    c = ModeTimer(someController, 1)
    c.update()
    c.cancel()
    assert c. isMainMode() is True


def test_menuMode_cancelInMainModeShouldDoNothing():
    c = ModeTimer(someController, 1)
    c.cancel()
    assert c. isMainMode() is True
