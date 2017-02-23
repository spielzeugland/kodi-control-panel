import time
import sys
import traceback
from threading import Thread
import messages
import controller


class Output(object):

    def __init__(self, controller):
        self._controller = controller

    def writePlayer(self, controller):
        print("Player")

    def writeMenu(self, controller):
        menu = controller.menu
        if menu.isRoot():
            folder = "Menu"
        else:
            folder = menu.folder().name()
        item = menu.item()
        text = "{0} > {1} [{2}/{3}]".format(folder, item.name(), menu._currentIndex, len(menu._currentItems))
        print(text)

    def writeMessage(self, message):
        print("Message: {0}".format(message))

    def clear(self):
        pass


class Input(object):

    def __init__(self, controller):
        self._controller = controller
        self._shouldStop = False
        self._configure()

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
