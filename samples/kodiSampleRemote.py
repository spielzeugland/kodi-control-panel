import context
import main
from console import Console
from menu import Menu, Folder, BackItem
from controller import Controller, Mode
from kodiMenu import AddonFolder, FavouritesFolder, ShutdownAction, RebootAction
from proxy import Server
from kodi import Kodi


if __name__ == "__main__":
    host = "http://osmc/jsonrpc"
    user = "osmc"
    pwd = "osmc"

    rpcProxy = Server(host, auth=(user, pwd))
    kodi = Kodi(rpcProxy)

    shutdownFolder = Folder("Shutdown", [ShutdownAction(kodi, "Now"), RebootAction(kodi)])
    rootFolder = Folder("root", [AddonFolder(kodi), FavouritesFolder(kodi), shutdownFolder])

    menu = Menu(rootFolder, BackItem())
    controller = Controller(None, menu)

    console = Console(controller)
    inputs = console
    display = console
    main.start(kodi, controller, inputs, display)
