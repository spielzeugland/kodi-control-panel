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
	def __init__(self, timeout=5):
		self._mode = ModeTimer.MainMode
		self._timer = None
		self._timeout = timeout
	def mode(self):
		return self._mode	
	def _timerFunction(self):
		# TODO lock "_mode"
		self._mode = ModeTimer.MainMode
	def update(self):
		if(self._mode is ModeTimer.MainMode):
			self._mode = ModeTimer.MenuMode
			self._timer = Timer(self._timeout, self._timerFunction)
			self._timer.setDaemon(True)
			self._timer.start()
			return False
		else:
			if(self._timer is not None):
				self._timer.cancel()
				self._timer = Timer(self._timeout, self._timerFunction)
				self._timer.setDaemon(True)
				self._timer.start()
				return True
			return True
