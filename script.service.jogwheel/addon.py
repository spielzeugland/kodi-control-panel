import xbmc
import lib.generic.events as events
import lib.generic.kodi as kodi
import lib.configuredMenu as configuredMenu
from lib.display import Display
from lib.inputs import Inputs


if __name__ == "__main__":
    try:
        localKodi = kodi.local(xbmc)

        queue = events.createQueue()

        inputs = Inputs(queue)
        display = Display()

        theController = configuredMenu.create(localKodi, display.update)

        queue.worker.start(theController.handle)

        monitor = localKodi.getMonitor()
        while not monitor.abortRequested():
            if monitor.waitForAbort(10):
                break

        # TODO exception handling
        # except Exception as e:
        #   display.write("Error")
    finally:
        if(inputs is not None):
            inputs.close()
