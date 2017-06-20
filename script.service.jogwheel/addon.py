import xbmc
import lib.generic.worker as worker
import lib.generic.configuredLogging as configuredLogging
import lib.generic.events as events
import lib.generic.kodi as kodi
import lib.configuredMenu as configuredMenu
from lib.display import Display
from lib.inputs import Inputs


if __name__ == "__main__":

    try:
        configuredLogging.configure(configuredLogging.WARNING, kodi.KodiLogHandler(xbmc))

        localKodi = kodi.local(xbmc)

        queue = worker.createQueue()

        inputs = Inputs(queue)
        display = Display()

        theController = configuredMenu.create(localKodi, display.update)
        theController.work(queue)

        monitor = localKodi.getMonitor()
        while not monitor.abortRequested():
            if monitor.waitForAbort(10):
                display.writeMessage("Good Bye!")
                break
            if not queue.worker.is_alive():
                localKodi.shutdown()

        # TODO exception handling
        # except Exception as e:
        #   display.write("Error")
    finally:
        if(inputs is not None):
            inputs.close()
