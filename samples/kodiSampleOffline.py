import context
import main
from _menus import kodiMainFolder as menuMainFolder
from menu import Menu
from controller import Controller, BackItem
from console import Console
from kodi import Kodi

if __name__ == "__main__":
    kodi = Kodi(None, None)

    backItem = BackItem()
    menu = Menu(menuMainFolder, backItem)
    controller = Controller(None, menu)
    backItem.controller = controller

    console = Console(controller)
    inputs = console
    display = console
    main.start(kodi, controller, inputs, display)
