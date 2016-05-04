# TODO adapt proper python module structure (test config currently requires "src.")
from modeTimer import ModeTimer

class Controller:
	MainMode = ModeTimer.MainMode
	MenuMode = ModeTimer.MenuMode
	def __init__(self, player, menu, timer=ModeTimer()):
		self.player = player
		self.menu = menu
		self._timer = timer
	def select(self):
		if(self._timer.update()):
			self.menu.select()
	def moveBy(self, offset):
		if(self._timer.update()):
			self.menu.moveBy(offset)
	def back(self):
		if(self._timer.update()):
			self.menu.back()
	def mode(self):
		return self._timer.mode()

