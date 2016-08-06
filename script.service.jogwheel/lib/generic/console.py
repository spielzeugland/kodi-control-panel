import time
import sys
import traceback
from threading import Thread
import messages
import controller


class Console(object):

    def __init__(self, controller):
        self._controller = controller
        self._shouldStop = False
        self._prevMode = None
        self._prevFolder = None
        self._prevItem = None
        self._configure()

    def update(self):
        menu = self._controller.menu
        mode = self._controller.mode()
        folder = menu.folder()
        item = menu.item()
        if mode is not self._prevMode or folder is not self._prevFolder or item is not self._prevItem:
            if mode is controller.Mode.Player:
                print("Player")
            else:
                print("Menu: {0} > {1} [{2}/{3}]".format(folder.name(), item.name(), menu._currentIndex, len(menu._currentItems)))
            self._prevMode = mode
            self._prevFolder = folder
            self._prevItem = item
        if messages.hasUnread():
            unreadMessages = messages.getUnread()
            if len(unreadMessages) > 0:
                print("Messages:")
                for message in unreadMessages:
                    print(message.text)
                    if message.sysInfo:
                        traceback.print_exception(message.sysInfo[0], message.sysInfo[1], message.sysInfo[2])

    def write(self, string):
        print(string)

    def clear(self):
        pass

    def _run(self):
        cmd = ""
        while not self._shouldStop and not cmd == "exit":
            cmd = self._read()
            if cmd == "x":
                self._controller.moveBy(1)
            elif cmd == "xx":
                self._controller.moveBy(2)
            elif cmd == "y":
                self._controller.moveBy(-1)
            elif cmd == "yy":
                self._controller.moveBy(-2)
            elif cmd == "s":
                self._controller.select()
            elif cmd == "b":
                self._controller.back()
            elif cmd == "r":
                self._controller.exitMenuMode()
            elif cmd == "exit":
                self.close()
            elif cmd == "help":
                self._printHelp()
            else:
                print("Unknown command: %s" % cmd)
                self._printHelp()

    def shutdown(self):
        return self._shouldStop

    def _configure(self):
        thread = Thread(target=self._run)
        thread.setDaemon(True)
        thread.start()

    def _printHelp(self):
                print("Available Commands:")
                print("  x      Next")
                print("  y      Previous")
                print("  s      Select")
                print("  b      Back")
                print("  r      Reset")
                print("  exit   Shutdown")
                print("  yy     2xPrevious")
                print("  xx     2xNext")

    def _read(self):
        try:
            return raw_input()
        except NameError:
            return input()

    def close(self):
        self._shouldStop = True
