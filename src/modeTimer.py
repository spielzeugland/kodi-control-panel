from threading import Timer

class ModeTimer:
	def __init__(self, timeout=5):
		self._mainMode = True
		self._timer = None
		self._timeout = timeout
	def isMainMode(self):
		return self._mainMode	
	def _timerFunction(self):
		# TODO lock "_mainMode"
		self._mainMode = True
	def update(self):
		if(self._mainMode is True):
			self._mainMode = False
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
