from generic.menu import Menu, Folder, BackItem
from generic.controller import Controller, Mode
from generic.kodiMenu import AddonFolder, FavouritesFolder, ShutdownAction, RebootAction


class _Player(object):

    def __init__(self, kodi):
        self._kodi = kodi

    def item(self):
        item = self._kodi.getCurrentItem()
        if item is None:
            item = {}
        return item


def create(kodi, controllerListener):
    shutdownFolder = Folder("Shutdown", [ShutdownAction(kodi, "Now"), RebootAction(kodi)])
    # TODO make configurable
    audioAddons = AddonFolder(kodi, "Music")
    videoAddons = AddonFolder(kodi, "Video", contentType="video")
    rootFolder = Folder("root", [FavouritesFolder(kodi), audioAddons, videoAddons, shutdownFolder])

    menu = Menu(rootFolder, BackItem())
    controller = Controller(_Player(kodi), menu, controllerListener)

    return controller
