from time import sleep

import context
import menu
import mocksKodi as kodi

class Action(menu.Action):
	def __init__(self, name):
		self._name = name
		self.runCnt = 0
	def name(self):
		return self._name
	def run(self, menu):
		self.runCnt += 1
		print("Executing %s" % self._name)

class Folder(menu.Folder):
	def __init__(self, name, items):
		self._name = name
		self._items = items
	def name(self):
		return self._name
	def items(self):
		return self._items

class DynamicFolder(menu.DynamicFolder):
	def __init__(self, name, items, loadingTimeout=0):
		super().__init__(name)
		self._items = items
		self._loadingTimeout = loadingTimeout
	def items(self):
		sleep(self._loadingTimeout)	
		return self._items
	def isDynamic(self):
		return True

class SynchronItemLoader:
	loadItemsStack = []
	def __init__(self):
		# reset for each new instance
		SynchronItemLoader.loadItemStack = []
	def loadItems(self, menu, folder):
		menu._updateItemsForFolder(folder, folder.items())
		SynchronItemLoader.loadItemsStack.append(folder)

class NeverItemLoader:
	def loadItems(self, menu, folder):
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

