import time
from src.controller import Controller

class Menu:
	def __init__(self):
		self.selectCount = 0
	def select(self):
		self.selectCount += 1 

def test_initialMode():
	c = Controller(None, Menu(), 1)
	assert c.mode() == Controller.MainMode
	
def test_interactionShouldEnableMenuMode():
	c = Controller(None, Menu(), 1)
	c.select()
	assert c.mode() is Controller.MenuMode

def test_selectInMainModeShouldNotDelegateToMenu():
	menu = Menu()
	c = Controller(None, menu, 1)
	c.select()
	assert menu.selectCount == 0

def test_selectInMenuModeShouldDelegateToMenu():
	menu = Menu()
	c = Controller(None, menu, 1)
	c.select()
	c.select()
	assert menu.selectCount == 1

def test_menuModeShouldBeExitedAfterTimeout():
	c = Controller(None, Menu(), 0.2)
	c.select()
	assert c.mode() is Controller.MenuMode
	time.sleep(0.5)
	assert c.mode() is Controller.MainMode

def test_interactionShouldExtendMenuMode():
	c = Controller(None, Menu(), 0.5)
	c.select()
	assert c.mode() is Controller.MenuMode
	time.sleep(0.3)
	c.select()
	assert c.mode() is Controller.MenuMode
	c.select()
	time.sleep(0.3)
	assert c.mode() is Controller.MenuMode
	c.select()
	time.sleep(0.7)
	assert c.mode() is Controller.MainMode
