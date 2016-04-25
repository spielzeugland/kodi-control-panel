from src.menu import Menu
from consoleDisplay import ConsoleDisplay

class Action:
	def __init__(self, name):
		self._name = name
	def name(self):
		return self._name
	def run(self):
		print("Executing %s" % self._name)
class Folder:
	def __init__(self, name, items):
		self._name = name
		self._items = items
	def name(self):
		return self._name
	def items(self):
		return self._items

backItem = Action("..")

folder1a = Folder("Empty Sub Folder 1", [])
folder1b = Folder("Empty Sub Folder 2", [])
folder1 = Folder("Folder 1", [folder1a, folder1b])
folder2a = Folder("Empty Sub Folder 1", [])
folder2b = Folder("Empty Sub Folder 2", [])
folder2 = Folder("Folder 2", [folder2a, folder2b])
a1 = Action("Action 1")
a2 = Action("Action 2")
a3 = Action("Action 3")
folder3 = Folder("Folder 3", [a1, a2, a3])		
emptyFolder = Folder("Folder with no entries", [])
mainFolder = Folder("Main Menu", [folder1, folder2, folder3, emptyFolder])

menu = Menu(mainFolder, backItem)
ConsoleDisplay(menu).open()
