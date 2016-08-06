import context
import messages
import traceback
from _consoleDisplay import ConsoleDisplay
from _menus import kodiMainFolder as menuMainFolder
from menu import Menu
from controller import Controller, Mode, BackItem

if __name__ == "__main__":
    backItem = BackItem()
    menu = Menu(menuMainFolder, backItem)
    controller = Controller(None, menu)

    backItem.controller = controller

    prevMode = None
    prevFolder = None
    prevItem = None

    def action():
        global prevMode
        global prevFolder
        global prevItem

        mode = controller.mode()
        folder = menu.folder()
        item = menu.item()
        if mode is not prevMode or folder is not prevFolder or item is not prevItem:
            if mode is Mode.Player:
                print("Player")
            else:
                print("Menu >>> %s > %s [%s/%s]" % (folder.name(), item.name(), menu._currentIndex, len(menu._currentItems)))
            prevMode = mode
            prevFolder = folder
            prevItem = item
        if messages.hasUnread():
            unreadMessages = messages.getUnread()
            if len(unreadMessages) > 0:
                print("Messages:")
                for message in unreadMessages:
                    print(message.text)
                    if message.sysInfo:
                        traceback.print_exception(message.sysInfo[0], message.sysInfo[1], message.sysInfo[2])

    console = ConsoleDisplay(controller, action)
    console.open()
