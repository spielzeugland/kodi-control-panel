from generic.menu import Menu, Folder
from generic.controller import Controller, Mode, BackItem
from generic.kodiMenu import AddonFolder, FavouritesFolder, ShutdownAction, RebootAction


def create(kodi):
    shutdownFolder = Folder("Shutdown", [ShutdownAction(kodi, "Now"), RebootAction(kodi)])
    # TODO make configurable
    rootFolder = Folder("root", [AddonFolder(kodi), FavouritesFolder(kodi), shutdownFolder])
    backItem = BackItem()

    menu = Menu(rootFolder, backItem)
    controller = Controller(None, menu)
    backItem.controller = controller

    return controller
