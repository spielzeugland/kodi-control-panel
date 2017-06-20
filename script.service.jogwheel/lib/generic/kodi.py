import json
import logging
from time import sleep
from proxy import Proxy, TransportError, ProtocolError
import configuredLogging


class Kodi:

    def __init__(self, rpcProxy, xbmc):
        self._proxy = rpcProxy
        if(xbmc is not None):
            self._monitor = xbmc.Monitor()
        else:
            self._monitor = _SimpleMonitor()

    def getAddons(self, contentType="audio"):
        response = self._proxy.Addons.GetAddons(content=contentType)
        return _noneAsEmptyList(response["addons"])

    def getFavourites(self):
        properties = ["window", "path", "windowparameter"]
        # response = self._proxy.Favourites.GetFavourites(type="media", properties=properties)
        response = self._proxy.Favourites.GetFavourites(properties=properties)
        return _noneAsEmptyList(response["favourites"])

    def getAddonDetails(self, addonId):
        response = self._proxy.Addons.GetAddonDetails(addonid=addonId, properties=["name"])
        return response["addon"]

    def getFiles(self, url):
        properties = ["title", "file"]
        response = self._proxy.Files.GetDirectory(properties=properties, directory=url, media="files")
        return _noneAsEmptyList(response["files"])

    def play(self, url):
        params = {"file": url}
        response = self._proxy.Player.Open(item=params)

    def getCurrentItem(self):
        players = self._proxy.Player.GetActivePlayers()
        if len(players) > 0:
            playerid = players[0]["playerid"]
            properties = ["title", "album", "artist", "season", "episode", "duration", "showtitle", "tvshowid", "file", "streamdetails"]
            response = self._proxy.Player.GetItem(properties=properties, playerid=playerid)
            return response["item"]  # ["label"]
        return None

    def shutdown(self):
        self._proxy.System.Shutdown()

    def reboot(self):
        self._proxy.System.Reboot()

    def getMonitor(self):
        return self._monitor


def _noneAsEmptyList(entries):
    if entries is None:
        entries = []
    return entries


def local(xbmc):
    instance = Kodi(_Local(xbmc), xbmc)
    return instance


class _Local(Proxy):

    def __init__(self, xbmc):
        self._xbmc = xbmc

    def send_request(self, method_name, is_notification, params):
        if is_notification:
            raise ProtocolError('Kodi does not support notifications for local JSON-RPC calls')

        request_body = self.serialize(method_name, params, is_notification)
        try:
            response = self._xbmc.executeJSONRPC(request_body)
        except Exception as requests_exception:
            raise TransportError('Error calling method %r' % method_name, requests_exception)

        responseJson = json.loads(response)
        return self.parse_result(responseJson)


class KodiLogHandler(logging.Handler):

    def __init__(self, xbmc):
        self._xbmc = xbmc
        msgFormat = '%(name)s:%(lineno)d: %(message)s'
        formatter = logging.Formatter(format=msgformat)
        self.setFormatter(formatter)

    def emit(self, record):
        msg = self.format(record)
        level = self._convert(record.level)
        self._xbmc.log(msg, level=logLevel)

    def _convertLevel(self, level):
        if level >= logging.CRITICAL:
            return _xbmc.LOGFATAL
        elif level >= logging.ERROR:
            return _xbmc.LOGERROR
        elif level >= logging.WARNING:
            return _xbmc.LOGWARNING
        elif level >= logging.INFO:
            # LOGINFO is considered to be more technical
            return _xbmc.LOGNOTICE
        elif level >= logging.DEBUG:
            return _xbmc.LOGDEBUG


class _SimpleMonitor(object):

    def abortRequested(self):
        return False

    def waitForAbort(self, timeToWait):
        sleep(timeToWait)
