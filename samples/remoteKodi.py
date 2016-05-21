import jsonrpc_requests as rpc

url = "http://osmc/jsonrpc"
user = "osmc"
pwd = "osmc"

server = rpc.Server(url, auth=(user, pwd))

class Kodi:
	def __init__(self):
		pass
	def getAddons(self):
		return server.Addons.GetAddons(content="audio")["addons"]
	def getFavourites(self):
		return server.Favourites.GetFavourites(type="media",properties=["window","path","windowparameter"])["favourites"]
	def getAddonDetails(self, addonId):
		return server.Addons.GetAddonDetails(addonid = addonId, properties = ["name"])["addon"]
	def getFiles(self, url):
		return server.Files.GetDirectory(properties = ["title", "file"], directory = url, media = "files")["files"]
	def play(self, url):
		params = {"file" : url}
		response = server.Player.Open(item=params)
	def getCurrentItem(self):
		players = server.Player.GetActivePlayers()
		if len(players) > 0:
			playerid = players[0]["playerid"]
			items = server.Player.GetItem(properties=["title", "album", "artist", "season", "episode", "duration", "showtitle", "tvshowid", "file", "streamdetails"], playerid=playerid)
			print(items)
			return items["item"]["label"]
		return None

