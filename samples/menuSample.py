from _consoleDisplay import ConsoleDisplay
from _menus import sampleMenu


menu = sampleMenu
prevFolder = None
prevItem = None


def action():
    global prevFolder
    global prevItem

    folder = menu.folder()
    item = menu.item()
    if folder is not prevFolder or item is not prevItem:
        print("%s > %s [%s/%s]" % (folder.name(), item.name(), menu._currentIndex, len(menu._currentItems)))
        prevFolder = folder
        prevItem = item

if __name__ == "__main__":
    console = ConsoleDisplay(menu, action)
    console.open()
