class Kodi:

    def __init__(self, proxy):
        self._proxy = proxy

    def getAddons(self):
        return self._proxy.Addons.GetAddons(content="audio")["addons"]

    def getFavourites(self):
        properties = ["window", "path", "windowparameter"]
        response = self._proxy.Favourites.GetFavourites(type="media", properties=properties)
        return response["favourites"]

    def getAddonDetails(self, addonId):
        response = self._proxy.Addons.GetAddonDetails(addonid=addonId, properties=["name"])
        return response["addon"]

    def getFiles(self, url):
        properties = ["title", "file"]
        response = self._proxy.Files.GetDirectory(properties=properties, directory=url, media "files")
        return response["files"]

    def play(self, url):
        params = {"file": url}
        response = self._proxy.Player.Open(item=params)

    def getCurrentItem(self):
        players = self._proxy.Player.GetActivePlayers()
        if len(players) > 0:
            playerid = players[0]["playerid"]
            properties = ["title", "album", "artist", "season", "episode", "duration", "showtitle", "tvshowid", "file", "streamdetails"]
            response = self._proxy.Player.GetItem(properties=properties, playerid=playerid)
            return response["item"]["label"]
        return None

    def shutdown(self):
        self._proxy.System.Shutdown()

    def reboot(self):
        self._proxy.System.Reboot()
