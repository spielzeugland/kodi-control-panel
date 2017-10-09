import menu
import worker
from timer import ExtensibleTimer as Timer


class Mode(object):
    Player = 0
    Menu = 1


class Controller(object):

    def __init__(self, player, menu, listener=None):
        self.player = player
        self.menu = menu
        self.menu.addListener(self)
        self._timer = Timer(lambda: self.exitMenuMode())
        self._listener = listener
        # TODO temporary approach for initial update of display
        self._notifyListener()

    def select(self):
        if self._timer.start():
            self.menu.select()
        self._notifyListener()

    def moveBy(self, offset):
        if self._timer.start():
            self.menu.moveBy(offset)
        self._notifyListener()

    def back(self):
        if self._timer.start():
            if self.menu.isRoot():
                self.exitMenuMode()
            else:
                self.menu.back()
                self._notifyListener()

    def exitMenuMode(self):
        self._timer.cancel()
        self._notifyListener()

    def mode(self):
        if self._timer.isRunning():
            return Mode.Menu
        else:
            return Mode.Player

    def _notifyListener(self):
        if self._listener is not None:
            self._listener(self)

    def work(self, queue):
        def _handle():
            event = queue.get()
            name = event["name"]
            if name is "moveBy":
                self.moveBy(event["data"])
                return True
            elif name is "click":
                self.select()
                return True
            elif name is "longClick":
                self.back()
                return True
            elif name is "veryLongClick":
                # TODO find better way to signal shutdown which also works with Kodi Monitors
                return False
        return worker.runAsLoop(_handle)

    def asyncMenuUpdate(self, menu):
        if self._timer.isRunning() is True:
            self._timer.start()
            self._notifyListener()
