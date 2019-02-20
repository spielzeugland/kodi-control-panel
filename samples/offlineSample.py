import _context
import _logConfig
import console
import _offlineMenu as configuredMenu
import menu
import worker
import controller
from kodi import Kodi
import simpleDisplay


_debug = True


if __name__ == "__main__":

    _logConfig.configure(_debug)

    kodi = Kodi(None, None)

    queue = worker.createQueue()

    inputs = console.Input(queue)
    display = simpleDisplay.Size20x4()
    display._debug = _debug

    theController = configuredMenu.create(kodi, display.update)
    theController.work(queue).join()
