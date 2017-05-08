from threading import Timer
from synchronized import createLock, withLock
import menu
import events


class Mode(object):
    Player = 0
    Menu = 1


class _ModeTimer(object):

    @createLock
    def __init__(self, controller, timeout=5):
        self._mainMode = True
        self._timer = None
        self._timeout = timeout
        self._controller = controller

    @withLock
    def isMainMode(self):
        return self._mainMode

    def _handleTimeout(self):
        self._backToMainMode()
        self._controller._notifyListener()

    @withLock
    def _backToMainMode(self):
        self._mainMode = True

    @withLock
    def update(self):
        if self._mainMode is True:
            self._mainMode = False
            self._timer = self._createAndStartTimer()
            return False
        else:
            if self._timer is not None:
                self._timer.cancel()
                self._timer = self._createAndStartTimer()
            return True

    @withLock
    def _createAndStartTimer(self):
        timer = Timer(self._timeout, self._handleTimeout)
        timer.setDaemon(True)
        timer.start()
        return timer

    @withLock
    def cancel(self):
        if self._timer is not None:
            self._timer.cancel()
            self._timer = None
        self._mainMode = True


class Controller(object):

    def __init__(self, player, menu, listener=None):
        self.player = player
        self.menu = menu
        self._timer = _ModeTimer(self)
        self._listener = listener
        # TODO temporary approach for initial update of display
        self._notifyListener()

    def select(self):
        if self._timer.update():
            self.menu.select()
        self._notifyListener()

    def moveBy(self, offset):
        if self._timer.update():
            self.menu.moveBy(offset)
        self._notifyListener()

    def back(self):
        if self._timer.update():
            if self.menu.isRoot():
                self.exitMenuMode()
            else:
                self.menu.back()
                self._notifyListener()

    def exitMenuMode(self):
        self._timer.cancel()
        self._notifyListener()

    def mode(self):
        if self._timer.isMainMode():
            return Mode.Player
        else:
            return Mode.Menu

    def _notifyListener(self):
        if self._listener is not None:
            self._listener(self)

    def handle(self, event):
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
