import _context
import console
import _configuredMenu as configuredMenu
import menu
import worker
import controller
from kodi import Kodi
import simpleDisplay
import time


_debug = True


def _print(msg):
    if _debug:
        t = time.asctime()
        print(("{0} >> {1}").format(t, msg))


if __name__ == "__main__":

    _print("sample starting")

    kodi = Kodi(None, None)

    queue = worker.createQueue()

    inputs = console.Input(queue)
    display = simpleDisplay.Size20x4()
    display._debug = _debug

    theController = configuredMenu.create(kodi, display.update)
    theController.work(queue).join()

    _print("sample stopped")
