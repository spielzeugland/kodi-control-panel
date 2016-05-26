import os, sys
sys.path.insert(0, os.path.abspath('../src'))

import menu
from time import sleep

class Action(menu.Action):
	def __init__(self, name):
		super().__init__(name)
	def run(self, menu):
		print("Executing %s" % self._name)

Folder = menu.Folder

class DynamicFolder(menu.DynamicFolder):
	def __init__(self, name, items, loadingTimeout=3):
		super().__init__(name)
		self._itemsToLoad = items
		self._loadingTimeout = loadingTimeout
	def _loadItems(self):
		sleep(self._loadingTimeout)
		return self._itemsToLoad

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

sampleMenu = menu.Menu(mainFolder, menu.BackItem())

cdTrack1 = Action("Track 1")
cdTrack2 = Action("Track 2")
cdTrack3 = Action("Track 3")
cd = DynamicFolder("CD", [cdTrack1, cdTrack2, cdTrack3], 5)
favs = Folder("Favourites", [])
webradio = Folder("Online radio", [])
settings = Folder("Settings", [])
shutdown = Action("Now")
reboot = Action("Restart")
end = Folder("Shutdown", [shutdown, reboot])
kodiMainFolder = Folder("Main", [cd, favs, webradio, settings, end])
kodiMenu = menu.Menu(kodiMainFolder, menu.BackItem())
