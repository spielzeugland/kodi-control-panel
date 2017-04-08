from generic.menu import Menu, Folder, BackItem
from generic.controller import Controller, Mode
from generic.kodiMenu import AddonFolder, FavouritesFolder, ShutdownAction, RebootAction


class _Player(object):

    def __init__(self, kodi):
        self._kodi = kodi

    def item(self):
        item = self._kodi.getCurrentItem()
        if item is None:
            item = "None"
        return item


def create(kodi, controllerListener):
    shutdownFolder = Folder("Shutdown", [ShutdownAction(kodi, "Now"), RebootAction(kodi)])
    # TODO make configurable
    rootFolder = Folder("root", [AddonFolder(kodi), FavouritesFolder(kodi), shutdownFolder])

    menu = Menu(rootFolder, BackItem())
    controller = Controller(_Player(kodi), menu, controllerListener)

    return controller
