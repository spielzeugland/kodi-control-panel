import os, sys
sys.path.insert(0, os.path.abspath('../src'))

from time import sleep
from menu import Menu, BackItem

class Action:
	def __init__(self, name):
		self._name = name
	def name(self):
		return self._name
	def run(self, menu):
		print("Executing %s" % self._name)

class Folder:
	def __init__(self, name, items):
		self._name = name
		self._items = items
	def name(self):
		return self._name
	def items(self):
		return self._items

class DynamicFolder:
	def __init__(self, name, items, loadingTimeout=0):
		self._name = name
		self._items = items
		self._loadingTimeout = loadingTimeout
		self._loaded = False
	def name(self):
		return self._name
	def items(self):
		if(self._loaded == False):
			sleep(self._loadingTimeout)
			self._loaded = True	
		return self._items
	def isDynamic(self):
		return not self._loaded

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

sampleMenu = Menu(mainFolder, BackItem())

cdTrack1 = Action("Track 1")
cdTrack2 = Action("Track 2")
cdTrack3 = Action("Track 3")
cd = DynamicFolder("CD", [cdTrack1, cdTrack2, cdTrack3], 5)
favs = Folder("Favourits", [])
webradio = Folder("Online radio", [])
settings = Folder("Settings", [])
shutdown = Action("Now")
reboot = Action("Restart")
end = Folder("Shutdown", [shutdown, reboot])
kodiMainFolder = Folder("Main", [cd, favs, webradio, settings, end])
kodiMenu = Menu(kodiMainFolder, BackItem())
