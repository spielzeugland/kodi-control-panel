from threading import Timer
from synchronized import createLock, withLock
import menu


class Mode(object):
    Player = 0
    Menu = 1


class _ModeTimer(object):

    @createLock
    def __init__(self, timeout=5):
        self._mainMode = True
        self._timer = None
        self._timeout = timeout

    @withLock
    def isMainMode(self):
        return self._mainMode

    @withLock
    def _backToMainMode(self):
        self._mainMode = True

    @withLock
    def update(self):
        if self._mainMode is True:
            self._mainMode = False
            self._timer = Timer(self._timeout, self._backToMainMode)
            self._timer.setDaemon(True)
            self._timer.start()
            return False
        else:
            if self._timer is not None:
                self._timer.cancel()
                self._timer = Timer(self._timeout, self._backToMainMode)
                self._timer.setDaemon(True)
                self._timer.start()
            return True

    @withLock
    def cancel(self):
        if self._timer is not None:
            self._timer.cancel()
            self._timer = None
        self._mainMode = True


class Controller(object):

    def __init__(self, player, menu, timer=_ModeTimer()):
        self.player = player
        self.menu = menu
        self._timer = timer

    def select(self):
        if self._timer.update():
            self.menu.select()

    def moveBy(self, offset):
        if self._timer.update():
            self.menu.moveBy(offset)

    def back(self):
        if self._timer.update():
            if self.menu.isRoot():
                self.exitMenuMode()
            else:
                self.menu.back()

    def mode(self):
        if self._timer.isMainMode():
            return Mode.Player
        else:
            return Mode.Menu

    def exitMenuMode(self):
        self._timer.cancel()
