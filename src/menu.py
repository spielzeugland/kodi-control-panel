from threading import Thread

class BackItem:
	def __init__(self, text=".."):
		self._text = text
	def name(self):
		return self._text
	def run(self, menu):
		menu.back()

class Folder:
	def __init__(self, name):
		self._name = name
	def name(self):
		return self._name
	
class DynamicFolder():
	def __init__(self, name):
		self._name = name
		self._items = None
	def name(self):
		return self._name
	def isDynamic(self):
		return self._items is None
	def items(self):
		if self.isDynamic():
			self._items = self._loadItems()
		return self._items
	def _loadItems(self):
		return []

class _EmptyItem:
	def name(self):
		return "<Empty>"
	def run(self, menu):
		pass

class _LoadingItem:
	def name(self):
		return "Loading..."
	def run(self, menu):
		pass

class _ItemLoader:
	def _run(self):
		# TODO error handling e.g. pass back item with error message
		items = self._folder.items()
		self._menu._updateItemsForFolder(self._folder, items)
	def loadItems(self, menu, folder):
		self._menu = menu
		self._folder = folder
		thread = Thread(target=self._run)
		thread.setDaemon(True)
		thread.start()

class Menu:
	def __init__(self, root, backItem = None, itemLoader = _ItemLoader):
		self._root = root
		self._menuStack = []
		self._backItem = backItem
		self._emptyItem = _EmptyItem()
		self._loadingItem = _LoadingItem()
		self._itemLoader = itemLoader
		self._setCurrentFolder(root)
	def _setCurrentFolder(self, folder, index = 0):
		self._currentFolder = folder
		if hasattr(folder.__class__, "items") and callable(getattr(folder.__class__, "items")):
			if hasattr(folder.__class__, "isDynamic") and callable(getattr(folder.__class__, "isDynamic")):
				self._updateItemsForFolder(folder, [self._loadingItem])
				self._itemLoader().loadItems(self, folder)
				return
			else:
				self._updateItemsForFolder(folder, folder.items(), index)
		else:
			self._currentItems = []
			self._currentIndex = 0
			# TODO log + message
	def _updateItemsForFolder(self, folder, items, index=0):
		if self._currentFolder is not folder:
			return
		# TODO check type of items to be a list
		self._currentItems = items
		if index > len(self._currentItems):
			self._currentIndex = 0
		else:
			self._currentIndex = index
	def moveBy(self, offset):
		length = len(self._currentItems)
		if self._backItem is not None:
			length += 1
		if length > 0:
			self._currentIndex = (self._currentIndex + offset) % length
		return self
	def select(self):
		length = len(self._currentItems)
		if self._currentIndex == length and self._backItem is not None:
			entry = self._backItem
		else:
			entry = self._currentItems[self._currentIndex]
		if hasattr(entry.__class__, "run") and callable(getattr(entry.__class__, "run")):
			# TODO error handling
			entry.run(self)
			return self
		else:
			stackTuple = (self._currentFolder, self._currentIndex)
			self._menuStack.append(stackTuple)
			self._setCurrentFolder(entry)
			return self
	def back(self):
		if len(self._menuStack) > 0:
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
		if self._currentIndex == length and self._backItem is not None:
			return self._backItem
		elif length > 0:
			return self._currentItems[self._currentIndex]
		return self._emptyItem
