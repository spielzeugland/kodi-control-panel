import _context
import _logConfig
from console import Console
import _offlineMenu as configuredMenu
import menu
import worker
import controller
import controllerWorker
from kodi import Kodi
import simpleDisplay


_debug = True


if __name__ == "__main__":

    _logConfig.configure(_debug)

    kodi = Kodi(None, None)

    queue = worker.createQueue()

    display = simpleDisplay.Size20x4()
    display._debug = _debug
    console = Console(queue, display)

    controller = configuredMenu.create(kodi, console.update)
    controllerWorker.start(queue, controller).join()
