import time
from src.modeTimer import ModeTimer

def test_construtorWithOptionalTimeout():
	c = ModeTimer()
	assert c._timeout == 5

def test_initial_shouldBeMainMode():
	c = ModeTimer(1)
	assert c.isMainMode() is True
	
def test_mainMode_updateShouldEnableMenuMode():
	c = ModeTimer(1)
	c.update()
	assert c.isMainMode() is False

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
	assert c.isMainMode() is False
	time.sleep(0.5)
	assert c.isMainMode() is True

def test_menuMode_updateShouldBeExtendMenuMode():
	c = ModeTimer(0.5)
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
	c = ModeTimer(1)
	c.update()
	c.cancel()
	assert c. isMainMode() is True

