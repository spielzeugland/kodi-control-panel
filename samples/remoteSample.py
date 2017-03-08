import getpass
import _context
import controller
import console
import events
import simpleDisplay
import configuredMenu
from proxy import Server
from kodi import Kodi


_debug = True


if __name__ == "__main__":
    host = "http://osmc:8080/jsonrpc"
    user = "osmc"
    pwd = getpass.getpass()

    rpcProxy = Server(host, auth=(user, pwd))
    kodi = Kodi(rpcProxy, None)

    queue = events.createQueue()

    inputs = console.Input(queue)
    display = simpleDisplay.Size20x4()
    display._debug = _debug

    theController = configuredMenu.create(kodi, display.update)

    queue.worker.start(theController.handle)

    queue.worker.join()
