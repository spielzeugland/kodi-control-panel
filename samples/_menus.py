import os
import sys
from time import sleep
import context
import menu
import messages


class Action(menu.Action):

    def __init__(self, name):
        super(Action, self).__init__(name)

    def run(self, menu):
        messages.add("Message from \"%s\"" % self.name())


class DynamicFolder(menu.DynamicFolder):

    def __init__(self, name, items, loadingTimeout=3):
        super(DynamicFolder, self).__init__(name)
        self._itemsToLoad = items
        self._loadingTimeout = loadingTimeout

    def _loadItems(self):
        sleep(self._loadingTimeout)
        return self._itemsToLoad


cdTrack1 = Action("Track 1")
cdTrack2 = Action("Track 2")
cdTrack3 = Action("Track 3")
cd = DynamicFolder("CD", [cdTrack1, cdTrack2, cdTrack3], 5)
favs = menu.Folder("Favourites", [])
station1 = Action("Station 1")
station2 = Action("Station 2")
station3 = Action("Station 3")
webradio = DynamicFolder("Online radio", [station1, station2, station3])
display = menu.Folder("Display", [])
sound = menu.Folder("Sound", [])
settings = menu.Folder("Settings", [display, sound])
shutdown = Action("Now")
reboot = Action("Restart")
end = menu.Folder("Shutdown", [shutdown, reboot])
kodiMainFolder = menu.Folder("Main", [cd, favs, webradio, settings, end])
kodiMenu = menu.Menu(kodiMainFolder, menu.BackItem())
