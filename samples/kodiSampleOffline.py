import context
import mainloop
from _menus import kodiMainFolder as menuMainFolder
from menu import Menu, BackItem
from controller import Controller
import console
from kodi import Kodi
import simpleDisplay


_debug = True

if __name__ == "__main__":
    mainloop._debug = _debug
    kodi = Kodi(None, None)

    menu = Menu(menuMainFolder, BackItem())
    controller = Controller(None, menu)

    inputs = console.Input(controller)
    display = simpleDisplay.Size20x4(controller)
    display._debug = _debug
    mainloop.start(kodi, controller, inputs, display)
