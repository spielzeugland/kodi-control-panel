from generic.menu import Menu, Folder, BackItem
from generic.controller import Controller, Mode
from generic.kodiMenu import AddonFolder, FavouritesFolder, ShutdownAction, RebootAction


def create(kodi, controllerListener):
    shutdownFolder = Folder("Shutdown", [ShutdownAction(kodi, "Now"), RebootAction(kodi)])
    # TODO make configurable
    rootFolder = Folder("root", [AddonFolder(kodi), FavouritesFolder(kodi), shutdownFolder])

    menu = Menu(rootFolder, BackItem())
    controller = Controller(None, menu, controllerListener)

    return controller
