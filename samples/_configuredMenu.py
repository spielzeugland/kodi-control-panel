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


class _AsyncFolder(menu.AsyncFolder):

    def __init__(self, name, items, loadingTimeout=2):
        super(_AsyncFolder, self).__init__(name)
        self._itemsToLoad = items
        self._loadingTimeout = loadingTimeout

    def _loadItems(self):
        sleep(self._loadingTimeout)
        return self._itemsToLoad


def create(kodi, controllerListener):
    cdTrack1 = _Action("Track 1")
    cdTrack2 = _Action("Track 2")
    cdTrack3 = _Action("Track 3")
    cd = _AsyncFolder("CD", [cdTrack1, cdTrack2, cdTrack3], 2)
    favs = menu.Folder("Favourites", [])
    station1 = _Action("Station 1")
    station2 = _Action("Station 2")
    station3 = _Action("Station 3")
    webradio = _AsyncFolder("Online radio", [station1, station2, station3], 5)
    display = menu.Folder("Display", [])
    sound = menu.Folder("Sound", [])
    longName = menu.Folder("A Folder with very long name should still be readable somehow", [])
    nameWithLineBreak = menu.Folder("linebreak: a\nb", [])
    special = menu.Folder("Edge-cases", [longName, nameWithLineBreak])
    settings = menu.Folder("Settings", [display, sound])
    shutdown = _Action("Now")
    reboot = _Action("Restart")
    end = menu.Folder("Shutdown", [shutdown, reboot])

    mainFolder = menu.Folder("Main", [cd, favs, webradio, settings, special, end])

    theMenu = menu.Menu(mainFolder)
    theController = controller.Controller(_OfflinePlayer(), theMenu, controllerListener)
    return theController
