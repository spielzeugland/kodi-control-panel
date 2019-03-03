import xbmc
import lib.generic.worker as worker
import lib.generic.controllerWorker as controllerWorker
import lib.generic.configuredLogging as configuredLogging
import lib.generic.kodi as kodi
import lib.configuredMenu as configuredMenu
from lib.hardware import Hardware


if __name__ == "__main__":

    inputs = None

    try:
        configuredLogging.configure(configuredLogging.WARNING, kodi.KodiLogHandler(xbmc))

        localKodi = kodi.local(xbmc)

        queue = worker.createQueue()

        hardware = Hardware(queue)

        controller = configuredMenu.create(localKodi, hardware.update)
        worker = controllerWorker.start(queue, controller)

        monitor = localKodi.getMonitor()
        while not monitor.abortRequested():
            if monitor.waitForAbort(10):
                break
            if not worker.is_alive():
                localKodi.shutdown()

        # TODO exception handling
        # except Exception as e:
        #   display.write("Error")
    finally:
        if(inputs is not None):
            inputs.close()
