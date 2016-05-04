from threading import Timer

# main mode (playing/idle)
# - displays what's currently playing
# - first interaction switches to menu mode
# menu mode
# - interactions delegated to menu
# - after X seconds back to main mode

class ModeTimer:
	MainMode = 0
	MenuMode = 1
	def __init__(self, menuModeTimeout=5):
		self._mode = ModeTimer.MainMode
		self._modeTimer = None
		self._menuModeTimeout = menuModeTimeout
	def mode(self):
		return self._mode	
	def _modeTimerFunction(self):
		# TODO lock "_mode"
		self._mode = ModeTimer.MainMode
	def update(self):
		if(self._mode is ModeTimer.MainMode):
			self._mode = ModeTimer.MenuMode
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
