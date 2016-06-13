import os
import sys
from time import sleep
import context
import menu


class Action(menu.Action):

    def __init__(self, name):
        super(Action, self).__init__(name)

    def run(self, menu):
        print("Executing %s" % self._name)


class DynamicFolder(menu.DynamicFolder):

    def __init__(self, name, items, loadingTimeout=3):
        super(DynamicFolder, self).__init__(name)
        self._itemsToLoad = items
        self._loadingTimeout = loadingTimeout

    def _loadItems(self):
        sleep(self._loadingTimeout)
        return self._itemsToLoad

folder1a = menu.Folder("Empty Sub Folder 1", [])
folder1b = menu.Folder("Empty Sub Folder 2", [])
folder1 = menu.Folder("Folder 1", [folder1a, folder1b])
folder2a = menu.Folder("Empty Sub Folder 1", [])
folder2b = menu.Folder("Empty Sub Folder 2", [])
folder2 = menu.Folder("Folder 2", [folder2a, folder2b])
a1 = Action("Action 1")
a2 = Action("Action 2")
a3 = Action("Action 3")
folder3 = menu.Folder("Folder 3", [a1, a2, a3])
emptyFolder = menu.Folder("Folder with no entries", [])
mainFolder = menu.Folder("Main Menu", [folder1, folder2, folder3, emptyFolder])
sampleMenu = menu.Menu(mainFolder, menu.BackItem())

cdTrack1 = Action("Track 1")
cdTrack2 = Action("Track 2")
cdTrack3 = Action("Track 3")
cd = DynamicFolder("CD", [cdTrack1, cdTrack2, cdTrack3], 5)
favs = menu.Folder("Favourites", [])
webradio = menu.Folder("Online radio", [])
settings = menu.Folder("Settings", [])
shutdown = Action("Now")
reboot = Action("Restart")
end = menu.Folder("Shutdown", [shutdown, reboot])
kodiMainFolder = menu.Folder("Main", [cd, favs, webradio, settings, end])
kodiMenu = menu.Menu(kodiMainFolder, menu.BackItem())
