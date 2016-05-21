import json
import time

def addFavourite(kodi, name ,url):
	fav = "{{\"type\": \"media\", \"title\": \"{0}\", \"path\": \"{1}\"}}".format(name, url)
	if len(kodi._favs) > 0:
		kodi._favs += ","
	kodi._favs += fav

def addAddon(kodi, name, addonId):
	addon = "{{\"addonid\": \"{0}\", \"type\": \"{0}\"}}".format(addonId)
	addonDetails = "{{\"type\": \"{0}\", \"addonid\": \"{0}\", \"name\": \"{1}\"}}".format(addonId, name)
	kodi._addons[addonId] = [addon, addonDetails]
	if len(kodi._allAddons) > 0:
		kodi._allAddons += ","
	kodi._allAddons += addon

def addFolder(kodi, folderUrl, name, url):
	_add(kodi, folderUrl, name, url, "directory")

def addFile(kodi, folderUrl, name, url):
	_add(kodi, folderUrl, name, url, "file")

def _add(kodi, folderUrl, name, url, fileType):
	file = "{{\"file\": \"{0}\", \"filetype\": \"{1}\", \"label\": \"{2}\"}}".format(url, fileType, name)
	if folderUrl not in kodi._files:
		kodi._files[folderUrl] = ""
	if len(kodi._files[folderUrl]) > 0:
		kodi._files[folderUrl] += ","
	kodi._files[folderUrl] += file

def addPlayDelay(kodi, delay):
	kodi._playDelay = delay
	
class Kodi:
	def __init__(self):
		self._addons = {}
		self._allAddons = ""
		self._files = {}
		self._favs = ""
		self._playUrl = None
		self._playCnt = 0
		self._playDelay = 0
	def getAddons(self):
		asJson = "{{\"addons\" : [{0}]}}".format(self._allAddons)
		return json.loads(asJson)["addons"]
	def getFavourites(self):
		asJson = "{{\"favs\" : [{0}]}}".format(self._favs)
		return json.loads(asJson)["favs"]
	def getAddonDetails(self, addonId):
		if addonId in self._addons:
			asJson = "{{\"addon\" : {0}}}".format(self._addons[addonId][1])
			return json.loads(asJson)["addon"]
		return []
	def getFiles(self, url):
		if url in self._files:
			asJson = "{{\"files\": [{0}]}}".format(self._files[url])
			return json.loads(asJson)["files"]
		return []
	def play(self, url):
		self._playCnt += 1
		self._playUrl = url
		time.sleep(self._playDelay)
	def playWasCalledWith(self, url):
		return self._playUrl == url
