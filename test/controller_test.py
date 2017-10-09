import context
import mocks
from controller import Controller, Mode


player = mocks.Player()
menu = mocks.Menu()
listenerOwner = mocks.ControllerListener()
listener = listenerOwner.update


def test_constructor():
    c = Controller(player, menu, listener)
    assert c.player is player
    assert c.menu is menu
    assert c._listener is listener


def test_modeShouldReturnPlayerModeDependingOnTimerMode():
    timer = mocks.notRunningTimer()
    c = Controller(player, menu, listener)
    c._timer = timer
    assert c.mode() is Mode.Player


def test_modeShouldReturnMenuModeDependingOnTimerMode():
    timer = mocks.runningTimer()
    c = Controller(player, menu, listener)
    c._timer = timer
    assert c.mode() is Mode.Menu


def test_playerMode_selectShouldNotDelegateToMenu():
    menu = mocks.Menu()
    c = Controller(player, menu, listener)
    c._timer = mocks.notRunningTimer()
    c.select()
    assert menu.selectCnt == 0


def test_menuMode_selectShouldDelegateToMenu():
    menu = mocks.Menu()
    c = Controller(player, menu, listener)
    c._timer = mocks.runningTimer()
    c.select()
    assert menu.selectCnt == 1


def test_playerMode_backShouldNotDelegateToMenu():
    menu = mocks.Menu()
    c = Controller(player, menu, listener)
    c._timer = mocks.notRunningTimer()
    c.back()
    assert menu.backCnt == 0


def test_menuMode_backOnRootFolder_shouldLeaveMenuMode():
    menu = mocks.Menu(isRoot=True)
    c = Controller(player, menu, listener)
    c._timer = mocks.runningTimer()
    c.back()
    assert menu.backCnt == 0


def test_menuMode_back_shouldDelegateToMenu():
    menu = mocks.Menu(isRoot=False)
    c = Controller(player, menu, listener)
    c._timer = mocks.runningTimer()
    c.back()
    assert menu.backCnt == 1


def test_playerMode_moveByShouldNotDelegateToMenu():
    menu = mocks.Menu()
    c = Controller(player, menu, listener)
    c._timer = mocks.notRunningTimer()
    c.moveBy(1)
    assert menu.moveByCnt == 0


def test_menuMode_moveByShouldDelegateToMenu():
    timer = mocks.runningTimer()
    c = Controller(player, mocks.Menu(), listener)
    c._timer = timer
    c.exitMenuMode()
    assert timer.cancelCnt == 1
