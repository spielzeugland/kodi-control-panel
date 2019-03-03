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
        self._messages = []
        self.menu.addListener(self._handleMenuUpdate)
        self._timer = Timer(lambda: self._exitMenuMode())
        self._listener = listener
        # TODO temporary approach for initial update of display
        self._notifyListener()

    def _select(self):
        if self._timer.start():
            self.menu.select()
        self._notifyListener()

    def _moveBy(self, offset):
        if self._timer.start():
            self.menu.moveBy(offset)
        self._notifyListener()

    def _back(self):
        if self._timer.start():
            if self.menu.isRoot():
                self._exitMenuMode()
            else:
                self.menu.back()
                self._notifyListener()

    def _exitMenuMode(self):
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
            moveCount = 0
            while name is "moveBy":
                moveCount = moveCount + event["data"]
                try:
                    event = queue.get(True, 0.1)
                    name = event["name"]
                except:
                    name = None
            if moveCount is not 0:
                self._moveBy(moveCount)
            if name is "click":
                self._select()
                return True
            elif name is "longClick":
                self._back()
                return True
            elif name is "veryLongClick":
                # TODO find better way to signal shutdown which also works with Kodi Monitors
                return False
        return worker.runAsLoop(_handle)

    def _handleMenuUpdate(self, menu, event):
        if self._timer.isRunning() is True:
            self._timer.start()
            self._notifyListener()
