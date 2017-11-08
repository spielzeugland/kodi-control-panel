from generic.menu import Menu, Folder
from generic.controller import Controller, Mode
from generic.kodiMenu import ChannelGroupFolder, ChannelFolder, AddonFolder, FavouritesFolder, ShutdownAction, RebootAction


class _Player(object):

    def __init__(self, kodi):
        self._kodi = kodi

    def item(self):
        item = self._kodi.getCurrentItem()
        if item is None:
            item = {}
        return item


def create(kodi, controllerListener):
    # TODO make structure configurable
    favs = FavouritesFolder(kodi)

    # channel structure is defined by the imported channel list
    tv = ChannelFolder(kodi, "TV", 1)  # use "All" for a flat list
    radio = ChannelGroupFolder(kodi, "Radio", "radio")

    videoAddons = AddonFolder(kodi, "Video", contentType="video")
    audioAddons = AddonFolder(kodi, "Music")
    shutdownFolder = Folder("Shutdown", [ShutdownAction(kodi, "Now"), RebootAction(kodi)])

    rootFolder = Folder("root", [favs, tv, radio, videoAddons, audioAddons, shutdownFolder])

    menu = Menu(rootFolder)
    controller = Controller(_Player(kodi), menu, controllerListener)

    return controller
