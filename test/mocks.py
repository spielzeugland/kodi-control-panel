class Menu():
	def __init__(self):
		self.selectCnt = 0
		self.backCnt = 0
		self.moveByCnt = 0
	def select(self):
		self.selectCnt += 1
	def back(self):
		self.backCnt += 1
	def moveBy(self):
		self.moveByCnt += 1

class Player:
	pass

class Timer():
	def __init__(self, interactionAllowed=False, mode=None):
		self._interactionAllowed = interactionAllowed
		self._mode = mode
		self.modeCnt = 0
	def update(self):
		return self._interactionAllowed
	def mode(self):
		self.modeCnt += 1 
		return self._mode

inMainMode = Timer(False)
inMenuMode = Timer(True)

