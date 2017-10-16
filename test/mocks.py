from time import sleep
import context
import menu
import proxy
import mocksKodi as kodi


class ControllerListener(object):

    def __init__(self):
        self.updateCount = 0

    def update(self, controller):
        self.updateCount += 1

    def reset(self):
        self.updateCount = 0


class Action(menu.Action):

    def __init__(self, name):
        super(Action, self).__init__(name)
        self.runCnt = 0

    def run(self, menu):
        self.runCnt += 1


class FailingAction(menu.Action):

    def __init__(self, name, exception):
        super(FailingAction, self).__init__(name)
        self._exception = exception

    def run(self, menu):
        raise self._exception


Folder = menu.Folder


class FailingFolder(menu.Folder):

    def __init__(self, name, exception):
        super(FailingFolder, self).__init__(name)
        self._exception = exception

    def items(self):
        raise self._exception


class IncorrectFolder(menu.Folder):

    def __init__(self, name):
        super(IncorrectFolder, self).__init__(name)

    def items(self):
        return "something which is not a list"


class AsyncFolder(menu.AsyncFolder):

    def __init__(self, name, items, delay=0):
        super(AsyncFolder, self).__init__(name)
        self._itemsToLoad = items
        self._delay = delay
        self.loadItemsCnt = 0

    def _loadItems(self):
        sleep(self._delay)
        self.loadItemsCnt += 1
        return self._itemsToLoad


class FailingAsyncFolder(menu.AsyncFolder):

    def __init__(self, name, exception):
        super(FailingAsyncFolder, self).__init__(name)
        self._exception = exception

    def _loadItems(self):
        raise self._exception


class SynchronAsyncFolder(AsyncFolder):

    def __init__(self, name, items, delay=0):
        super(SynchronAsyncFolder, self).__init__(name, items, delay)

    def items(self, callback=None):
        items = self._loadItems()
        if callback:
            callback(items)
        return items


class NeverLoadingFolder(AsyncFolder):

    def __init__(self, name, items, delay=0):
        super(NeverLoadingFolder, self).__init__(name, items, delay)

    def items(self, callback=None):
        pass


class Menu(object):

    def __init__(self, isRoot=True):
        self._isRoot = isRoot
        self.selectCnt = 0
        self.backCnt = 0
        self.moveByCnt = 0

    def select(self):
        self.selectCnt += 1

    def back(self):
        self.backCnt += 1

    def moveBy(self, offset):
        self.moveByCnt += 1

    def isRoot(self):
        return self._isRoot

    def addListener(self, listener):
        pass


class CountingMenuListener(object):

    def __init__(self):
        self.count = 0

    def asyncMenuUpdate(self, menu):
        self.count += 1


class Player(object):
    pass


class _ExtensibleTimer(object):

    def __init__(self, running=True):
        self._running = running
        self.cancelCnt = 0

    def start(self):
        return self._running

    def isRunning(self):
        return self._running

    def cancel(self):
        self.cancelCnt += 1


def notRunningTimer():
    return _ExtensibleTimer(running=False)


def runningTimer():
    return _ExtensibleTimer(running=True)


class Proxy(proxy.Proxy):

    def send_request(self, method_name, is_notification, params):
        pass


class Xbmc(object):

    LOGFATAL = 5
    LOGERROR = 4
    LOGWARNING = 3
    LOGNOTICE = 2
    LOGDEBUG = 1
    abortRequested = False

    def __init__(self):
        self.messages = []

    def log(self, msg, level):
        self.messages.append({"msg": msg, "level": level})

    class Monitor(object):

        def abortRequested(self):
            return Xbmc.abortRequested

        def waitForAbort(self, timeToWait):
            pass


class CountingMethod(object):

    def __init__(self, method=None):
        self.count = 0
        self._method = method

    def get(self):
        def m():
            self.count += 1
            if self._method is not None:
                return self._method()
        return m


def returnFalse():
    return False
