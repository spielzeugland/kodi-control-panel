import os, sys
sys.path.insert(0, os.path.abspath('../src'))

from consoleDisplay import ConsoleDisplay
from sampleMenu import sampleMenu
from controller import Controller, Mode

menu = sampleMenu
controller = Controller(None, sampleMenu)

prevMode = None
prevFolder = None
prevItem = None

def action():
	global menu
	global controller
	global prevMode
	global prevFolder
	global prevItem
	
	mode = controller.mode()
	folder = menu.folder()
	item = menu.item()
	if(mode is not prevMode or folder is not prevFolder or item is not prevItem):
		if(mode is Mode.Main):
			print("Player")
		else:
			print("Menu >>> %s > %s [%s/%s]" % (folder.name(), item.name(), menu._currentIndex, len(menu._currentItems)))
		prevMode = mode
		prevFolder = folder
		prevItem = item

console = ConsoleDisplay(controller, action)
console.open()
