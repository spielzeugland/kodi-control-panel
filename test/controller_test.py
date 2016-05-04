import mocks
from src.controller import Controller

player = mocks.Player()
menu = mocks.Menu()

def test_constructor():
	c = Controller(player, menu, mocks.Timer())
	assert c.player is player
	assert c.menu is menu

def test_constructorWithOptionalTimer():
	c = Controller(player, menu)

def test_modeShouldReturnMainModeFromTimer():
	timer = mocks.Timer(mode=Controller.MainMode)
	c = Controller(player, menu, timer)
	assert c.mode() == Controller.MainMode
	assert timer.modeCnt == 1

def test_modeShouldReturnMenuModeFromTimer():
	timer = mocks.Timer(mode=Controller.MenuMode)
	c = Controller(player, menu, timer)
	assert c.mode() == Controller.MenuMode
	assert timer.modeCnt == 1

def test_mainMode_selectShouldNotDelegateToMenu():
	menu = mocks.Menu()
	c = Controller(player, menu, mocks.inMainMode)
	c.select()
	assert menu.selectCnt == 0

def test_menuMode_selectShouldDelegateToMenu():
	menu = mocks.Menu()
	c = Controller(player, menu, mocks.inMenuMode)
	c.select()
	assert menu.selectCnt == 1

def test_mainMode_backShouldNotDelegateToMenu():
	menu = mocks.Menu()
	c = Controller(player, menu, mocks.inMainMode)
	c.back()
	assert menu.backCnt == 0

def test_menuMode_backShouldDelegateToMenu():
	menu = mocks.Menu()
	c = Controller(player, menu, mocks.inMenuMode)
	c.back()
	assert menu.backCnt == 1

def test_mainMode_moveByShouldNotDelegateToMenu():
	menu = mocks.Menu()
	c = Controller(player, menu, mocks.inMainMode)
	c.moveBy(1)
	assert menu.moveByCnt == 0

def test_menuMode_moveByShouldDelegateToMenu():
	menu = mocks.Menu()
	c = Controller(player, menu, mocks.inMenuMode)
	c.moveBy(1)
	assert menu.moveByCnt == 1

