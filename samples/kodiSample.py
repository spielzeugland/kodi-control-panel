import context
from _consoleDisplay import ConsoleDisplay
from menu import Menu, Folder, BackItem
from controller import Controller, Mode
from kodiMenu import AddonFolder, FavouritesFolder, ShutdownAction, RebootAction
from proxy import Server
from kodi import Kodi


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


if __name__ == "__main__":
    host = "http://osmc/jsonrpc"
    user = "osmc"
    pwd = "osmc"

    rpcProxy = Server(host, auth=(user, pwd))
    kodi = Kodi(rpcProxy)

    shutdownFolder = Folder("Shutdown", [ShutdownAction(kodi, "Now"), RebootAction(kodi)])

    mainFolder = Folder("root", [AddonFolder(kodi), FavouritesFolder(kodi), shutdownFolder])

    backItem = BackItem()
    menu = Menu(mainFolder, backItem)
    controller = Controller(None, menu)
    backItem.controller = controller

    console = ConsoleDisplay(controller, action)
    console.open()
