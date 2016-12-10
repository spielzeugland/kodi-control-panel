import context
import main
from _menus import kodiMainFolder as menuMainFolder
from menu import Menu, BackItem
from controller import Controller
from console import Console
from kodi import Kodi

if __name__ == "__main__":
    kodi = Kodi(None, None)

    menu = Menu(menuMainFolder, BackItem())
    controller = Controller(None, menu)

    console = Console(controller)
    inputs = console
    display = console
    main.start(kodi, controller, inputs, display)
