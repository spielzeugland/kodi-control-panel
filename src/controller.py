from threading import Timer

# main mode (playing/idle)
# - displays what's currently playing
# - first interaction switches to menu mode
# menu mode
# - interactions delegated to menu
# - after X seconds back to main mode

# TODO stopped here: refactor to ModeTimer -> independent of menu etc. Controller will own this timer
class Controller:
	MainMode = 0
	MenuMode = 1
	def __init__(self, player, menu, menuModeTimeout=5):
		self._mode = Controller.MainMode
		self._modeTimer = None
		self._player = player
		self._menu = menu
		self._menuModeTimeout = menuModeTimeout
	def moveBy(self, offset):
		if(self._updateModeTimer()):
			self._menu.moveBy(offset)
	def select(self):
		if(self._updateModeTimer()):
			self._menu.select()
	def back(self):
		if(self._updateModeTimer()):
			self._menu.back()
	def mode(self):
		return self._mode
	def _modeTimerFunction(self):
		# TODO lock "_mode"
		self._mode = Controller.MainMode
	def _updateModeTimer(self):
		if(self._mode is Controller.MainMode):
			self._mode = Controller.MenuMode
			self._modeTimer = Timer(self._menuModeTimeout, self._modeTimerFunction)
			self._modeTimer.setDaemon(True)
			self._modeTimer.start()
			return False
		else:
			if(self._modeTimer is not None):
				self._modeTimer.cancel()
				self._modeTimer = Timer(self._menuModeTimeout, self._modeTimerFunction)
				self._modeTimer.setDaemon(True)
				self._modeTimer.start()
				return True
			return True
