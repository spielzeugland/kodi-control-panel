from controller import Mode
import messages
import traceback


def start(kodi, controller, inputs, display):
    display.writeMessage("Welcome")
    _mainloop(kodi, controller, inputs, display)
    display.writeMessage("Shuting down...")


def _mainloop(kodi, controller, inputs, display):
    monitor = kodi.getMonitor()
    while not inputs.shutdown() and not monitor.abortRequested():

        # TODO using simple polling in a mainloop for now
        _update(display, controller)

        if monitor.waitForAbort(0.1):
            break


_prevMode = None
_prevFolder = None
_prevItem = None
_debug = False


def _update(display, controller):
    global _prevMode
    global _prevFolder
    global _prevItem
    global _debug

    menu = controller.menu
    mode = controller.mode()
    folder = menu.folder()
    item = menu.item()
    if mode is not _prevMode or folder is not _prevFolder or item is not _prevItem:
        if mode is Mode.Player:
            display.writePlayer(controller)
        else:
            display.writeMenu(controller)
        _prevMode = mode
        _prevFolder = folder
        _prevItem = item
    if _debug:
        _writeMessages()


def _writeMessages():
    if messages.hasUnread():
        unreadMessages = messages.getUnread()
        if len(unreadMessages) > 0:
            print("Messages:")
            for message in unreadMessages:
                print(message.text)
                if message.sysInfo:
                    traceback.print_exception(message.sysInfo[0], message.sysInfo[1], message.sysInfo[2])
