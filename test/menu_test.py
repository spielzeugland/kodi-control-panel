from src.menu import Menu

class Action:
	def __init__(self, name):
		self._name = name
	def name(self):
		return self._name
	def run(self):
		pass
class Folder:
	def __init__(self, name, items):
		self._name = name
		self._items = items
	def name(self):
		return self._name
	def items(self):
		return self._items

backItem = Action("<Back>")
		
folder1a = Folder("F1a", [])
folder1b = Folder("F1b", [])
folder1 = Folder("F1", [folder1a, folder1b])
folder2a = Folder("F2a", [])
folder2b = Folder("F2b", [])
folder2 = Folder("F2", [folder2a, folder2b])
a1 = Action("A1")
a2 = Action("A2")
a3 = Action("A3")
folder3 = Folder("Folder", [a1, a2, a3])		
mainFolder = Folder("Nested", [folder1, folder2, folder3])

emptyFolder = Folder("Folder with no entries", [])		

def test_init_shouldSelectFirstItemInRootFolder():
	menu = Menu(mainFolder)
	assert menu.folder() is mainFolder
	assert menu.item() is folder1

def test_moveBy0_shouldDoNothing():
	menu = Menu(mainFolder)
	menu.moveBy(0)
	assert menu.item() is folder1
def test_moveBy1():
	menu = Menu(mainFolder)
	menu.moveBy(1)
	assert menu.item() is folder2
def test_moveBy3():
	menu = Menu(mainFolder)
	menu.moveBy(3)
	assert menu.item() is folder1
def test_moveBy4():
	menu = Menu(mainFolder)
	menu.moveBy(4)
	assert menu.item() is folder2
def test_moveByMinus1():
	menu = Menu(mainFolder)
	menu.moveBy(-1)
	assert menu.item() is folder3

def test_moveBy0_withBackItem_shouldDoNothing():
	menu = Menu(mainFolder, backItem)
	menu.moveBy(0)
	assert menu.item() is folder1
def test_moveBy1_withBackItem():
	menu = Menu(mainFolder, backItem)
	menu.moveBy(1)
	assert menu.item() is folder2
def test_moveBy3_withBackItem():
	menu = Menu(mainFolder, backItem)
	menu.moveBy(3)
	assert menu.item() is backItem
def test_moveBy4_withBackItem():
	menu = Menu(mainFolder, backItem)
	menu.moveBy(4)
	assert menu.item() is folder1
def test_moveByMinus1_withBackItem():
	menu = Menu(mainFolder, backItem)
	menu.moveBy(-1)
	assert menu.item() is backItem
def test_moveByMinus2_withBackItem():
	menu = Menu(mainFolder, backItem)
	menu.moveBy(-2)
	assert menu.item() is folder3

def test_moveBy1_shouldNotFailForEmptyFolder():
	menu = Menu(emptyFolder)
	menu.moveBy(1)
	assert menu.item() is menu._emptyItem
def test_moveBy0_shouldNotFailForEmptyFolder():
	menu = Menu(emptyFolder)
	menu.moveBy(0)
	assert menu.item() is menu._emptyItem
def test_moveByMinus1_shouldNotFailForEmptyFolder():
	menu = Menu(emptyFolder)
	menu.moveBy(-1)
	assert menu.item() is menu._emptyItem

def test_moveBy1_withBackItem_shouldNotFailForEmptyFolder():
	menu = Menu(emptyFolder, backItem)
	menu.moveBy(1)
	assert menu.item() is backItem
def test_moveBy0_withBackItem_shouldNotFailForEmptyFolder():
	menu = Menu(emptyFolder, backItem)
	menu.moveBy(0)
	assert menu.item() is backItem
def test_moveByMinus1_withBackItem_shouldNotFailForEmptyFolder():
	menu = Menu(emptyFolder, backItem)
	menu.moveBy(-1)
	assert menu.item() is backItem

def test_select_shouldOpenFolder():
	menu = Menu(mainFolder)
	menu.select()
	assert menu.folder() is folder1
def test_select_shouldOpenFolderAndShowItsFirstEntry():
	menu = Menu(mainFolder)
	menu.moveBy(1)
	menu.select()
	assert menu.folder() is folder2
	assert menu.item() is folder2a
def test_select_multiLevel():
	menu = Menu(mainFolder)
	menu.moveBy(1).select().moveBy(1).select()
	assert menu.folder() is folder2b

def test_back():
	menu = Menu(mainFolder)
	menu.select()
	menu.back()
	assert menu.folder() is mainFolder
def test_back_shouldRemeberIndex():
	menu = Menu(mainFolder)
	menu.moveBy(1)
	menu.select()
	menu.back()
	assert menu.item() is folder2
def test_back_shouldDoNothingForRootFolder():
	menu = Menu(mainFolder)
	menu.back().back()
	assert menu.folder() is mainFolder
def test_back_multiLevel():
	menu = Menu(mainFolder)
	menu.moveBy(1).select().moveBy(1).select()
	menu.back()
	assert menu.folder() is folder2
	assert menu.item() is folder2b
	menu.back()
	assert menu.folder() is mainFolder
	assert menu.item() is folder2

def test_reset_shouldGoToFirstItemOfMainFolder():
	menu = Menu(mainFolder)
	menu.moveBy(1).select().moveBy(1).select()
	menu.reset()
	assert menu.folder() is mainFolder
	assert menu.item() is folder1
	assert len(menu._menuStack) == 0