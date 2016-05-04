class _EmptyItem:
	def name():
		return "<Empty>"
	def items():
		return []
# Menu
#  Action: name, run
#  Folder: name, items
class Menu:
	def __init__(self, root, backItem = None):
		self._root = root
		self._menuStack = []
		self._emptyItem = _EmptyItem()
		self._backItem = backItem
		self._setCurrentFolder(root)
	def _setCurrentFolder(self, folder, index = 0):
		self._currentFolder = folder
		self._currentIndex = index
		if(hasattr(folder.__class__, "items") and callable(getattr(folder.__class__, "items"))):
			self._currentItems = folder.items()
		else:
			self._currentItems = []
			self._currentIndex = 0
			# TODO log + message
	def moveBy(self, offset):
		length = len(self._currentItems)
		if(self._backItem is not None):
			length += 1
		if length > 0:
			self._currentIndex = (self._currentIndex + offset) % length
		return self
	def select(self):
		length = len(self._currentItems)
		if(self._currentIndex == length and self._backItem is not None):
			self.back()
			return self
		entry = self._currentItems[self._currentIndex]
		if(hasattr(entry.__class__, "run") and callable(getattr(entry.__class__, "run"))):
			# TODO error handling
			entry.run(self)
		else:
			self._menuStack.append([self._currentFolder, self._currentIndex])
			self._setCurrentFolder(entry)
			return self
	def back(self):
		if(len(self._menuStack) > 0):
			parent = self._menuStack.pop()
			self._setCurrentFolder(parent[0], parent[1])
		return self
	def reset(self):
		self._setCurrentFolder(self._root)
		self._menuStack.clear()
		return self
	def folder(self):
		return self._currentFolder
	def item(self):
		length = len(self._currentItems)
		if(self._currentIndex == length and self._backItem is not None):
			return self._backItem
		elif(length > 0):
			return self._currentItems[self._currentIndex]
		return self._emptyItem