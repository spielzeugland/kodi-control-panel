from menu import DynamicFolder, Action, AsyncAction
from threading import Thread


class UrlFile(AsyncAction):

    def __init__(self, kodi, name, url):
        super(UrlFile, self).__init__(name)
        self._kodi = kodi
        self._url = url

    def _asyncRun(self):
        self._kodi.play(self._url)


class UrlFolder(DynamicFolder):

    def __init__(self, kodi, name, url):
        super(UrlFolder, self).__init__(name)
        self._kodi = kodi
        self._url = url

    def _loadItems(self):
        items = []
        files = self._kodi.getFiles(self._url)
        for file in files:
            name = file["label"]
            url = file["file"]
            filetype = file["filetype"]
            if filetype == "directory":
                folder = UrlFolder(self._kodi, name, url)
            elif filetype == "file":
                folder = UrlFile(self._kodi, name, url)
            else:
                # TODO handle unexpected filetype
                continue
            items.append(folder)
        return items


class AddonFolder(DynamicFolder):

    def __init__(self, kodi, name="Addons"):
        super(AddonFolder, self).__init__(name)
        self._kodi = kodi

    def _loadItems(self):
        items = []
        addons = self._kodi.getAddons()
        for addon in addons:
            addonId = addon["addonid"]
            details = self._kodi.getAddonDetails(addonId)
            name = details["name"]
            url = "plugin://{0}/".format(addonId)
            folder = UrlFolder(self._kodi, name, url)
            items.append(folder)
        return items


class FavouritesFolder(DynamicFolder):

    def __init__(self, kodi, name="Favourites"):
        super(FavouritesFolder, self).__init__(name)
        self._kodi = kodi

    def _loadItems(self):
        items = []
        favs = self._kodi.getFavourites()
        for fav in favs:
            name = fav["title"]
            url = fav["path"]
            folder = UrlFile(self._kodi, name, url)
            items.append(folder)
        return items


class ShutdownAction(Action):

    def __init__(self, kodi, text="Shutdown"):
        self._kodi = kodi
        super(ShutdownAction, self).__init__(text)

    def run(self, menu):
        self._kodi.shutdown()


class RebootAction(Action):

    def __init__(self, kodi, text="Reboot"):
        self._kodi = kodi
        super(RebootAction, self).__init__(text)

    def run(self, menu):
        self._kodi.reboot()
