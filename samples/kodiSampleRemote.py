import getpass
import context
import mainloop
import console
import simpleDisplay
import configuredMenu as configuredMenu
from proxy import Server
from kodi import Kodi


_debug = True


if __name__ == "__main__":
    host = "http://osmc:8080/jsonrpc"
    user = "osmc"
    pwd = getpass.getpass()

    rpcProxy = Server(host, auth=(user, pwd))
    kodi = Kodi(rpcProxy, None)

    controller = configuredMenu.create(kodi)

    inputs = console.Input(controller)
    display = simpleDisplay.Size20x4(controller)
    display._debug = _debug

    mainloop._debug = _debug
    mainloop.start(kodi, controller, inputs, display)
