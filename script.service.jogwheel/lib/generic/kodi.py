import log
import json
from time import sleep
from proxy import Proxy, TransportError, ProtocolError


class Kodi:

    def __init__(self, rpcProxy, xbmc):
        self._proxy = rpcProxy
        if(xbmc is not None):
            self._monitor = xbmc.Monitor()
        else:
            self._monitor = _SimpleMonitor()

    def getAddons(self):
        response = self._proxy.Addons.GetAddons(content="audio")
        return _noneAsEmptyList(response["addons"])

    def getFavourites(self):
        properties = ["window", "path", "windowparameter"]
        response = self._proxy.Favourites.GetFavourites(type="media", properties=properties)
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
    # TODO pass AddOn or it's id as argument
    log.set(Log("script.service.jogwheel", xbmc))
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

        parsed = json.loads(response)
        return self.parse_result(parsed)


class Log(object):

    def __init__(self, name, xbmc):
        self._name = name
        self._xbmc = xbmc

    def error(self, msg, *args):
        self._log(self._xbmc.LOGERROR, msg, *args)

    def warning(self, msg, *args):
        self._log(self._xbmc.LOGWARNING, msg, *args)

    def info(self, msg, *args):
        self._log(self._xbmc.LOGNOTICE, msg, *args)

    def debug(self, msg, *args):
        self._log(self._xbmc.LOGDEBUG, msg, *args)

    def _log(self, logLevel, msg, *args):
        parameters = [self._name, msg] + args
        self._xbmc.log("### [%s] - %s" .format(parameters), level=logLevel)  # TODO add all arguments


class _SimpleMonitor(object):

    def abortRequested(self):
        return False

    def waitForAbort(self, timeToWait):
        sleep(timeToWait)
