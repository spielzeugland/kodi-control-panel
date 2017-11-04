from bisect import insort
from menu import CountingFolder, Folder, AsyncFolder, Action, AsyncAction


class Default(object):

    def __init__(self, folder, length):
        self._items = []
        self._folder = folder
        self._length = length

    def add(self, item):
        self._items.append(item)

    def asList(self):
        return self._items


class _Sorted(Default):

    def add(self, item):
        insort(self._items, item)


def Sorted(minSize=0, default=Default):
    def create(folder, length):
        if length >= minSize:
            return _Sorted(folder, length)
        else:
            return default(folder, length)
    return create


class _Grouped(Default):

    def __init__(self, folder, length):
        super(_Grouped, self).__init__(folder, length)
        self._groupIndex = {}

    def add(self, item):
        name = item.name()
        if len(name) > 0:
            self._addToGroup(name[0].upper(), item)
        else:
            self._addToGroup("")

    def _addToGroup(self, name, item):
        group = self._groupIndex.get(name)
        if group is None:
            group = CountingFolder(name, [])
            insort(self._items, group)
            self._groupIndex[name] = group
        insort(group._items, item)

    def asList(self):
        if len(self._groupIndex) == 1:
            return self._items[0].items()
        else:
            return self._items


def Grouped(minSize=0, default=Default):
    def create(folder, length):
        if length >= minSize:
            return _Grouped(folder, length)
        else:
            return default(folder, length)
    return create


class KodiFolder(AsyncFolder):

    def __init__(self, kodi, name, structure=Default):
        super(KodiFolder, self).__init__(name)
        self._kodi = kodi
        self._structure = structure


class UrlFile(AsyncAction):

    def __init__(self, kodi, name, url):
        super(UrlFile, self).__init__(name)
        self._kodi = kodi
        self._url = url

    def _asyncRun(self):
        self._kodi.play(self._url)


class UrlFolder(KodiFolder):

    def __init__(self, kodi, name, url, structure=Default):
        super(UrlFolder, self).__init__(kodi, name, structure)
        self._url = url

    def _loadItems(self):
        files = self._kodi.getFiles(self._url)
        items = self._structure(self, len(files))
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
            items.add(folder)
        return items.asList()


class AddonFolder(KodiFolder):

    def __init__(self, kodi, name="Addons", contentType="audio", structure=Sorted(0)):
        super(AddonFolder, self).__init__(kodi, name, structure)
        self._contentType = contentType

    def _loadItems(self):
        addons = self._kodi.getAddons(self._contentType)  # TODO add tests for contentType usage
        items = self._structure(self, len(addons))
        for addon in addons:
            addonId = addon["addonid"]
            details = self._kodi.getAddonDetails(addonId)
            name = details["name"]
            url = "plugin://{0}/".format(addonId)
            folder = UrlFolder(self._kodi, name, url)
            items.add(folder)
        return items.asList()


class FavouritesFolder(KodiFolder):

    def __init__(self, kodi, name="Favourites", structure=Sorted(0)):
        super(FavouritesFolder, self).__init__(kodi, name, structure)

    def _loadItems(self):
        favs = self._kodi.getFavourites()
        items = self._structure(self, len(favs))
        for fav in favs:
            name = fav["title"]
            if fav["type"] == "media":
                url = fav["path"]
                folder = UrlFile(self._kodi, name, url)
                items.add(folder)
            elif fav["type"] == "window":
                url = fav["windowparameter"]
                folder = UrlFolder(self._kodi, name, url)
                items.add(folder)
            else:
                # ignoring script&unknown for now
                continue
        return items.asList()


class ChannelGroupFolder(KodiFolder):

    def __init__(self, kodi, name, channelType, structure=Default):
        super(ChannelGroupFolder, self).__init__(kodi, name, structure)
        self._channelType = channelType

    def _loadItems(self):
        groups = self._kodi.getChannelGroups(self._channelType)
        items = self._structure(self, len(groups))
        for group in groups:
            id = group["channelgroupid"]
            name = group["label"]
            folder = ChannelFolder(self._kodi, name, id)
            items.add(folder)
        return items.asList()


class ChannelFolder(KodiFolder):

    def __init__(self, kodi, name, groupId, structure=Default):
        super(ChannelFolder, self).__init__(kodi, name, structure)
        self._groupId = groupId

    def _loadItems(self):
        channels = self._kodi.getChannels(self._groupId)
        items = self._structure(self, len(channels))
        for channel in channels:
            id = channel["channelid"]
            name = channel["label"]
            folder = ChannelItem(self._kodi, name, id)
            items.add(folder)
        return items.asList()


class ChannelItem(AsyncAction):

    def __init__(self, kodi, name, id):
        super(ChannelItem, self).__init__(name)
        self._kodi = kodi
        self._id = id

    def _asyncRun(self):
        self._kodi.playChannel(self._id)


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
