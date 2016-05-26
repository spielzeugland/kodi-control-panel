from time import sleep

import context
import menu
import mocksKodi as kodi

class Action(menu.Action):
	def __init__(self, name):
		super().__init__(name)
		self.runCnt = 0
	def run(self, menu):
		self.runCnt += 1

Folder = menu.Folder

class DynamicFolder(menu.DynamicFolder):
	def __init__(self, name, items, delay=0):
		super().__init__(name)
		self._itemsToLoad = items
		self._delay = delay
		self.loadItemsCnt = 0
	def items(self, callback=None):
		super.items(callback)
	def _loadItems(self):
		sleep(self._delay)
		self.loadItemsCnt += 1	
		return self._itemsToLoad
		
class SynchronDynamicFolder(DynamicFolder):
	def __init__(self, name, items, delay=0):
		super().__init__(name, items, delay)
	def items(self, callback=None):
		items = self._loadItems()
		if callback:
			callback(items)
		return items

class NeverLoadingFolder(DynamicFolder):
	def __init__(self, name, items, delay=0):
		super().__init__(name, items, delay)
	def items(self, callback=None):
		pass

class Menu():
	def __init__(self):
		self.selectCnt = 0
		self.backCnt = 0
		self.moveByCnt = 0
		self.updateItemsStack = []
	def select(self):
		self.selectCnt += 1
	def back(self):
		self.backCnt += 1
	def moveBy(self, offset):
		self.moveByCnt += 1
	def _updateItemsForFolder(self, folder, items, index = 0):
		self.updateItemsStack.append([folder, items, index])

class Player:
	pass

class Timer():
	def __init__(self, mainMode=True):
		self._mainMode = mainMode
		self.isMainModeCnt = 0
		self.cancelCnt = 0
	def update(self):
		return not self._mainMode
	def isMainMode(self):
		self.isMainModeCnt += 1 
		return self._mainMode
	def cancel(self):
		self.cancelCnt += 1

def timerInMainMode():
	return Timer(mainMode = True)

def timerInMenuMode():
	return Timer(mainMode = False)

