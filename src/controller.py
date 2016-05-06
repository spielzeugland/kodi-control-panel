from enum import Enum, unique
from modeTimer import ModeTimer

@unique
class Mode(Enum):
	Player = 0
	Menu = 1

class Controller:
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
		if (self._timer.isMainMode()):
			return Mode.Player
		else:
			return Mode.Menu
