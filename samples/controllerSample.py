import os, sys
sys.path.insert(0, os.path.abspath('../src'))

from consoleDisplay import ConsoleDisplay
from sampleMenu import kodiMainFolder as menuMainFolder
from menu import Menu
from controller import Controller, Mode, BackItem

backItem = BackItem()
menu = Menu(menuMainFolder, backItem)
controller = Controller(None, menu)

backItem.controller = controller

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
			print("Player")
		else:
			print("Menu >>> %s > %s [%s/%s]" % (folder.name(), item.name(), menu._currentIndex, len(menu._currentItems)))
		prevMode = mode
		prevFolder = folder
		prevItem = item

console = ConsoleDisplay(controller, action)
console.open()
