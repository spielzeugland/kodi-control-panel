import os
import sys
from time import sleep
import _context
import controller
import menu_old as menu


class _OfflinePlayer(object):

    def item(self):
        return {"title": "<Offline Player>"}


class _Action(menu.Action):

    def __init__(self, name):
        super(_Action, self).__init__(name)

    def run(self):
        print(">> Message from \"{0}\"".format(self.name()))


class _SlowFolder(menu.Folder):

    def __init__(self, name, items, loadingTimeout=2):
        super(_SlowFolder, self).__init__(name)
        self._itemsToLoad = items
        self._loadingTimeout = loadingTimeout

    def items(self):
        sleep(self._loadingTimeout)
        return self._itemsToLoad

class _FailingFolder(menu.Folder):

    def __init__(self, name):
        super(_FailingFolder, self).__init__(name)
        self._cnt = 0

    def items(self):
        self._cnt = self._cnt + 1
        msg = "Exception [{0}] from \"{1}\"".format(self._cnt, self._name)
        print(msg)
        raise Exception(msg)


class _FailingAction(menu.Action):

    def __init__(self, name):
        super(_FailingAction, self).__init__(name)

    def run(self):
        raise Exception("Exception from \"{0}\"".format(self.name()))


def create(kodi, listener):
    cdTrack1 = _Action("Track 1")
    cdTrack2 = _Action("Track 2")
    cdTrack3 = _Action("Track 3")
    cd = _SlowFolder("CD", [cdTrack1, cdTrack2, cdTrack3], 2)
    favs = menu.Folder("Favourites", [])
    station1 = _Action("Station 1")
    station2 = _Action("Station 2")
    station3 = _Action("Station 3")
    webradio1 = _SlowFolder("Online radio (fast)", [station1, station2, station3], 2)
    webradio2 = _SlowFolder("Online radio (slow)", [station1, station2, station3], 5)
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

    rootFolder = menu.Folder("Main Menu", [cd, favs, webradio1, webradio2, settings, special, end])

    theController = controller.Controller(_OfflinePlayer(), rootFolder, listener)
    return theController
