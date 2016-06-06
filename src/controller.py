from threading import Timer
from enum import Enum, unique


@unique
class Mode(Enum):
    Player = 0
    Menu = 1


class _ModeTimer:

    def __init__(self, timeout=5):
        self._mainMode = True
        self._timer = None
        self._timeout = timeout

    def isMainMode(self):
        return self._mainMode

    def _timerFunction(self):
        self._mainMode = True

    def update(self):
        if self._mainMode is True:
            self._mainMode = False
            self._timer = Timer(self._timeout, self._timerFunction)
            self._timer.setDaemon(True)
            self._timer.start()
            return False
        else:
            if self._timer is not None:
                self._timer.cancel()
                self._timer = Timer(self._timeout, self._timerFunction)
                self._timer.setDaemon(True)
                self._timer.start()
                return True

            return True

    def cancel(self):
        if self._timer is not None:
            self._timer.cancel()
        self._mainMode = True


class Controller:

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
            self.menu.back()

    def mode(self):
        if self._timer.isMainMode():
            return Mode.Player
        else:
            return Mode.Menu

    def exitMenuMode(self):
        self._timer.cancel()
