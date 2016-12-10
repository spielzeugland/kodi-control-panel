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
        print("Executing \"%s\"" % self.name())


class DynamicFolder(menu.DynamicFolder):

    def __init__(self, name, items, loadingTimeout=3):
        super(DynamicFolder, self).__init__(name)
        self._itemsToLoad = items
        self._loadingTimeout = loadingTimeout

    def _loadItems(self):
        sleep(self._loadingTimeout)
        return self._itemsToLoad


class MessageAction(menu.Action):

    def __init__(self, name):
        super(MessageAction, self).__init__(name)

    def run(self, menu):
        messages.add("Message from \"%s\"" % self.name())


cdTrack1 = Action("Track 1")
cdTrack2 = Action("Track 2")
cdTrack3 = Action("Track 3")
cd = DynamicFolder("CD", [cdTrack1, cdTrack2, cdTrack3], 5)
favs = menu.Folder("Favourites", [])
webradio = menu.Folder("Online radio", [])
settings = menu.Folder("Settings", [])
shutdown = MessageAction("Now")
reboot = MessageAction("Restart")
end = menu.Folder("Shutdown", [shutdown, reboot])
kodiMainFolder = menu.Folder("Main", [cd, favs, webradio, settings, end])
kodiMenu = menu.Menu(kodiMainFolder, menu.BackItem())
