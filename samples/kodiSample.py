import os, sys
sys.path.insert(0, os.path.abspath('../src'))

from consoleDisplay import ConsoleDisplay
from sampleMenu import Folder
from menu import Menu, BackItem
from controller import Controller, Mode
from kodiMenu import AddonFolder, FavouritesFolder, ShutdownAction, RebootAction
from remoteKodi import Kodi

kodi = Kodi("http://osmc/jsonrpc", "osmc", "osmc")

shutdownFolder = Folder("Shutdown", [ShutdownAction(kodi, "Now"), RebootAction(kodi)])

mainFolder = Folder("root", [AddonFolder(kodi), FavouritesFolder(kodi), shutdownFolder])

customBackItem = BackItem()
menu = Menu(mainFolder, customBackItem)
controller = Controller(None, menu)

def backItemRun(menu):
	if(menu.folder() is mainFolder):
		controller.exitMenuMode()
		menu.reset()
	else:
		menu.back()

customBackItem.run = backItemRun

prevMode = None
prevFolder = None
prevItem = None

def action():
	global prevMode
	global prevFolder
	global prevItem
	
	mode = controller.mode()
	folder = menu.folder()
	item = menu.item()
	if mode is not prevMode or folder is not prevFolder or item is not prevItem:
		if mode is Mode.Player:
			print("Playing: {0}".format(kodi.getCurrentItem()))
		else:
			print("Menu: {0} > {1} [{2}/{3}]".format(folder.name(), item.name(), menu._currentIndex, len(menu._currentItems)))
		prevMode = mode
		prevFolder = folder
		prevItem = item

console = ConsoleDisplay(controller, action)
console.open()
