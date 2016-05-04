from consoleDisplay import ConsoleDisplay
from sampleMenu import sampleMenu

menu = sampleMenu
prevFolder = None
prevItem = None

def action():
	folder = menu.folder()
	item = menu.item()
	if(folder is not prevFolder or item is not prevItem):
		print("%s > %s [%s/%s]" % (folder.name(), item.name(), menu._currentIndex, len(menu._currentItems)))
		prevFolder = folder
		prevItem = item

console = ConsoleDisplay(menu, action)
console.start()
