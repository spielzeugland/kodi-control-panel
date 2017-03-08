import xbmc
import lib.generic.events as events
import lib.generic.kodi as kodi
import lib.configuredMenu as menu
from lib.display import Display
from lib.inputs import Inputs


if __name__ == "__main__":
    try:
        localKodi = kodi.local(xbmc)
        controller = menu.create(localKodi)

        queue = events.createQueue

        inputs = Inputs(controller, queue)
        display = Display()

        queue.worker.start(controller.handle)
        # TODO use kodi monitor for proper shutdown handling
        # queue.worker.join()

    except Exception as e:
        # TODO exception handling
        display.write("Error")
    finally:
        if(inputs is not None):
            inputs.close()
