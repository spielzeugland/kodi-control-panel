import os
import sys
from time import sleep
import _context
import controller
import menu
import messages


class _OfflinePlayer(object):

    def item(self):
        return {"title": "<Offline Player>"}


class _Action(menu.Action):

    def __init__(self, name):
        super(_Action, self).__init__(name)

    def run(self, menu):
        messages.add("Message from \"%s\"" % self.name())


class _DynamicFolder(menu.DynamicFolder):

    def __init__(self, name, items, loadingTimeout=3):
        super(_DynamicFolder, self).__init__(name)
        self._itemsToLoad = items
        self._loadingTimeout = loadingTimeout

    def _loadItems(self):
        sleep(self._loadingTimeout)
        return self._itemsToLoad


def create(kodi, controllerListener):
    cdTrack1 = _Action("Track 1")
    cdTrack2 = _Action("Track 2")
    cdTrack3 = _Action("Track 3")
    cd = _DynamicFolder("CD", [cdTrack1, cdTrack2, cdTrack3], 5)
    favs = menu.Folder("Favourites", [])
    station1 = _Action("Station 1")
    station2 = _Action("Station 2")
    station3 = _Action("Station 3")
    webradio = _DynamicFolder("Online radio", [station1, station2, station3])
    display = menu.Folder("Display", [])
    sound = menu.Folder("Sound", [])
    longName = menu.Folder("A Folder with very long name should still be readable somehow", [])
    settings = menu.Folder("Settings", [display, sound])
    shutdown = _Action("Now")
    reboot = _Action("Restart")
    end = menu.Folder("Shutdown", [shutdown, reboot])

    mainFolder = menu.Folder("Main", [cd, favs, webradio, settings, longName, end])

    theMenu = menu.Menu(mainFolder, menu.BackItem())
    theController = controller.Controller(_OfflinePlayer(), theMenu, controllerListener)
    return theController
