class Kodi:
	def __init__(self, proxy):
		self._proxy = proxy
	def getAddons(self):
		return self._proxy.Addons.GetAddons(content="audio")["addons"]
	def getFavourites(self):
		return self._proxy.Favourites.GetFavourites(type="media",properties=["window","path","windowparameter"])["favourites"]
	def getAddonDetails(self, addonId):
		return self._proxy.Addons.GetAddonDetails(addonid = addonId, properties = ["name"])["addon"]
	def getFiles(self, url):
		return self._proxy.Files.GetDirectory(properties = ["title", "file"], directory = url, media = "files")["files"]
	def play(self, url):
		params = {"file" : url}
		response = self._proxy.Player.Open(item=params)
	def getCurrentItem(self):
		players = self._proxy.Player.GetActivePlayers()
		if len(players) > 0:
			playerid = players[0]["playerid"]
			items = self._proxy.Player.GetItem(properties=["title", "album", "artist", "season", "episode", "duration", "showtitle", "tvshowid", "file", "streamdetails"], playerid=playerid)
			return items["item"]["label"]
		return None
	def shutdown(self):
		self._proxy.System.Shutdown()
	def reboot(self):
		self._proxy.System.Reboot()
