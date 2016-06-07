import time
from threading import Thread


class ConsoleDisplay:

    def __init__(self, menuOrController, action):
        self._object = menuOrController
        self._action = action
        self._shouldStop = False

    def _run(self):
        while not self._shouldStop:
            time.sleep(0.5)
            self._action()

    def open(self):
        thread = Thread(target=self._run)
        thread.setDaemon(True)
        thread.start()
        cmd = ""
        while cmd != "exit":
            cmd = input()
            if cmd == "x":
                self._object.moveBy(1)
            elif cmd == "xx":
                self._object.moveBy(2)
            elif cmd == "y":
                self._object.moveBy(-1)
            elif cmd == "yy":
                self._object.moveBy(-2)
            elif cmd == "s":
                self._object.select()
            elif cmd == "b":
                self._object.back()
            elif cmd == "r":
                if(hasattr(self._object.__class__, "reset")):
                    self._object.reset()
                elif(hasattr(self._object.__class__, "exitMenuMode")):
                    self._object.exitMenuMode()
            elif cmd == "exit":
                self.close()
            elif cmd == "help":
                print("Available Commands:")
                print("  x      Next")
                print("  y      Previous")
                print("  s      Select")
                print("  b      Back")
                print("  r      Reset")
                print("  exit   2xNext")
                print("  yy     2xPrevious")
                print("  xx     2xNext")

    def close(self):
        self._shouldStop = True
