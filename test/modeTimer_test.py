import time
from src.modeTimer import ModeTimer

def test_initial_shouldBeMainMode():
	c = ModeTimer(1)
	assert c.mode() == ModeTimer.MainMode
	
def test_mainMode_updateShouldEnableMenuMode():
	c = ModeTimer(1)
	c.update()
	assert c.mode() is ModeTimer.MenuMode

def test_mainMode_updateShouldReturnFalse():
	c = ModeTimer(1)
	assert False == c.update()

def test_menuMode_updateShouldReturnTrue():
	c = ModeTimer(1)
	c.update()
	assert True == c.update()

def test_menuMode_shouldBeExitedAfterTimeout():
	c = ModeTimer(0.2)
	c.update()
	assert c.mode() is ModeTimer.MenuMode
	time.sleep(0.5)
	assert c.mode() is ModeTimer.MainMode

def test_menuMode_updateShouldBeExtendMenuMode():
	c = ModeTimer(0.5)
	c.update()
	assert c.mode() is ModeTimer.MenuMode
	time.sleep(0.3)
	c.update()
	assert c.mode() is ModeTimer.MenuMode
	c.update()
	time.sleep(0.3)
	assert c.mode() is ModeTimer.MenuMode
	c.update()
	time.sleep(0.7)
	assert c.mode() is ModeTimer.MainMode
