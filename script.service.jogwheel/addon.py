import xbmc
import lib.generic.kodi as kodi
import lib.main as main
import lib.configuredMenu as menu
from lib.display import Display
from lib.inputs import Inputs


if __name__ == "__main__":
    try:
        localKodi = kodi.local(xbmc)
        controller = menu.create(localKodi)
        inputs = Inputs(controller)
        display = Display(controller)
        main.start(localKodi, controller, inputs, display)
    except Exception as e:
        # TODO exception handling
        display.write("Error")
    finally:
        if(inputs is not None):
            inputs.close()
        if(display is not None):
            display.close()
