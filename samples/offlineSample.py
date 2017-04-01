import _context
import console
import events
import _configuredMenu as configuredMenu
import menu
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

    queue = events.createQueue()

    inputs = console.Input(queue)
    display = simpleDisplay.Size20x4()
    display._debug = _debug

    theController = configuredMenu.create(kodi, display.update)

    queue.worker.start(theController.handle)

    _print("sample started")

    queue.worker.join()

    _print("sample stopped")
