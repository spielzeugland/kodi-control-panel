import time
import sys
import traceback
import worker
import simpleDisplay

    
class Console(object):

    def __init__(self, queue, display):
        self._display = display
        self._inputs = _Inputs(queue, self._display)

    def update(self, event):
        self._display.update(event)

    def close(self):
        self._inputs.close()

    
class _Inputs(object):

    def __init__(self, queue, display):
        self._queue = queue
        self._display = display
        self._shouldStop = False
        self._configure()

    def _run(self):
        cmd = ""
        while not self._shouldStop and not cmd == "exit":
            cmd = self._read()
            if cmd == "x":
                self._queueEvent("moveBy", 1)
            elif cmd == "xx":
                self._queueEvent("moveBy", 2)
            elif cmd == "xxxx":
                steps = 123
                while steps > 0:
                    self._queueEvent("moveBy", 1)
                    steps = steps - 1
            elif cmd == "y":
                self._queueEvent("moveBy", -1)
            elif cmd == "yy":
                self._queueEvent("moveBy", -2)
            elif cmd == "s":
                self._queueEvent("click", self._display._currentItem)
            elif cmd == "b":
                self._queueEvent("longClick")
            #  elif cmd == "r":
            #     self._queueEvent("exitMenuMode")
            elif cmd == "exit":
                self._queueEvent("veryLongClick")
                # self.close()
            elif cmd == "help":
                self._printHelp()
            else:
                print("Unknown command: %s" % cmd)
                self._printHelp()

    def _queueEvent(self, event, data=None):
        self._queue.put_nowait({"name": event, "data": data})

    # TODO delete if not needed anymore
    def shutdown(self):
        return self._shouldStop

    def _configure(self):
        worker.runAsLoop(self._run)

    def _printHelp(self):
                print("Available Commands:")
                print("  x      Next")
                print("  xx     2x Next")
                print("  xxxx   123x Next")
                print("  y      Previous")
                print("  yy     2x Previous")
                print("  s      Select (click)")
                print("  b      Back (long click)")
                # print("  r      Reset")
                print("  exit   Shutdown (Very long click)")

    def _read(self):
        try:
            return raw_input()
        except NameError:
            return input()

    def close(self):
        self._shouldStop = True
