import os
import sys
from time import sleep
import _context
import controller
import menu


class _OfflinePlayer(object):

    def item(self):
        return {"title": "<Offline Player>"}


class _Action(menu.Action):

    def __init__(self, name):
        super(_Action, self).__init__(name)

    def run(self, menu):
        print(">> Message from \"{0}\"".format(self.name()))


class _AsyncFolder(menu.AsyncFolder):

    def __init__(self, name, items, loadingTimeout=2):
        super(_AsyncFolder, self).__init__(name)
        self._itemsToLoad = items
        self._loadingTimeout = loadingTimeout

    def _loadItems(self):
        sleep(self._loadingTimeout)
        return self._itemsToLoad


class _FailingFolder(menu.AsyncFolder):

    def __init__(self, name):
        super(_FailingFolder, self).__init__(name)
        self._cnt = 0

    def _loadItems(self):
        self._cnt = self._cnt + 1
        msg = "Exception [{0}] from \"{1}\"".format(self._cnt, self._name)
        print(msg)
        raise Exception(msg)


class _FailingAction(menu.Action):

    def __init__(self, name):
        super(_FailingAction, self).__init__(name)

    def run(self, menu):
        raise Exception("Exception from \"{0}\"".format(self.name()))


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
    folderWithError = _FailingFolder("folder with error")
    actionWithError = _FailingAction("action with error")
    special = menu.Folder("Edge-cases", [longName, nameWithLineBreak, folderWithError, actionWithError])
    settings = menu.Folder("Settings", [display, sound])
    shutdown = _Action("Now")
    reboot = _Action("Restart")
    end = menu.Folder("Shutdown", [shutdown, reboot])

    mainFolder = menu.Folder("Main", [cd, favs, webradio, settings, special, end])

    theMenu = menu.Menu(mainFolder)
    theController = controller.Controller(_OfflinePlayer(), theMenu, controllerListener)
    return theController
