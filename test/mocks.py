class Menu():
	def __init__(self):
		self.selectCnt = 0
		self.backCnt = 0
		self.moveByCnt = 0
	def select(self):
		self.selectCnt += 1
	def back(self):
		self.backCnt += 1
	def moveBy(self, offset):
		self.moveByCnt += 1

class Player:
	pass

class Timer():
	def __init__(self, mainMode=True):
		self._mainMode = mainMode
		self.isMainModeCnt = 0
	def update(self):
		return not self._mainMode
	def isMainMode(self):
		self.isMainModeCnt += 1 
		return self._mainMode

timerInMainMode = Timer(mainMode = True)
timerInMenuMode = Timer(mainMode = False)

