from time import sleep
import context
import menu
import proxy
import mocksKodi as kodi


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


class DynamicFolder(menu.DynamicFolder):

    def __init__(self, name, items, delay=0):
        super(DynamicFolder, self).__init__(name)
        self._itemsToLoad = items
        self._delay = delay
        self.loadItemsCnt = 0

    def _loadItems(self):
        sleep(self._delay)
        self.loadItemsCnt += 1
        return self._itemsToLoad


class FailingDynamicFolder(menu.DynamicFolder):

    def __init__(self, name, exception):
        super(FailingDynamicFolder, self).__init__(name)
        self._exception = exception

    def _loadItems(self):
        raise self._exception


class SynchronDynamicFolder(DynamicFolder):

    def __init__(self, name, items, delay=0):
        super(SynchronDynamicFolder, self).__init__(name, items, delay)

    def items(self, callback=None):
        items = self._loadItems()
        if callback:
            callback(items)
        return items


class NeverLoadingFolder(DynamicFolder):

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


class Player(object):
    pass


class Timer(object):

    def __init__(self, mainMode=True):
        self._mainMode = mainMode
        self.isMainModeCnt = 0
        self.cancelCnt = 0

    def update(self):
        return not self._mainMode

    def isMainMode(self):
        self.isMainModeCnt += 1
        return self._mainMode

    def cancel(self):
        self.cancelCnt += 1


def timerInMainMode():
    return Timer(mainMode=True)


def timerInMenuMode():
    return Timer(mainMode=False)


class Logging(object):

    def __init__(self):
        self.name = None
        self.recorded = {}

    def logger(self, loggerName):
        self.name = loggerName
        return self

    def error(self, message, *args):
        self.recorded["error"] = {"message": message, "args": args}

    def warning(self, message, *args):
        self.recorded["warning"] = {"message": message, "args": args}

    def info(self, message, *args):
        self.recorded["info"] = {"message": message, "args": args}

    def debug(self, message, *args):
        self.recorded["debug"] = {"message": message, "args": args}


class Proxy(proxy.Proxy):

    def send_request(self, method_name, is_notification, params):
        pass


class Xbmc(object):

    abortRequested = False

    class Monitor(object):

        def abortRequested(self):
            return Xbmc.abortRequested

        def waitForAbort(self, timeToWait):
            pass
