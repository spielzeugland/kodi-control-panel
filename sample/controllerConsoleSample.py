from consoleDisplay import ConsoleDisplay
from sampleMenu import sampleMenu
from src.controller import Controller

menu = sampleMenu
controller = Controller(None, sampleMenu)

prevMode = None
prevFolder = None
prevItem = None

def action():
	mode = controller.mode()
	folder = menu.folder()
	item = menu.item()
	if(mode is not prevMode or folder is not prevFolder or item is not prevItem):
		if(mode is Controller.MainMode):
			print("Player")
		elif:
			print("Menu >>> %s > %s [%s/%s]" % (folder.name(), item.name(), menu._currentIndex, len(menu._currentItems)))
		prevMode = mode
		prevFolder = folder
		prevItem = item

console = ConsoleDisplay(controller, action)
console.start()
