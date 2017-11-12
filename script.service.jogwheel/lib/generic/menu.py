import sys
from threading import RLock
import worker
from synchronized import createLock, withLock, injectLock
import configuredLogging as logging


class Action(object):

    def __init__(self, name):
        self._name = name

    def name(self):
        return self._name

    def run(self, menu):
        pass

    def __lt__(self, other):
        return self._name.lower() < other.name().lower()


class _BackItem(Action):

    def __init__(self, name=".."):
        super(_BackItem, self).__init__(name)

    def run(self, menu):
        menu.back()


class AsyncAction(Action):

    @createLock
    def __init__(self, name):
        super(AsyncAction, self).__init__(name)
        self._thread = None

    # TODO locking looks incorrect in this class
    def run(self, menu):
        if not self._isRunning():
            self._scheduleRun()

    @withLock
    def _scheduleRun(self):
        self._thread = worker.run(self._asyncRun)

    @withLock
    def _isRunning(self):
        return self._thread is not None and self._thread.is_alive()

    def _asyncRun(self):
        pass


class Folder(object):

    def __init__(self, name, items=[]):
        self._name = name
        self._items = items

    def name(self):
        return self._name

    def items(self):
        return self._items

    def __lt__(self, other):
        return self._name.lower() < other.name().lower()


class CountingFolder(Folder):

    def name(self):
        return "{0} ({1})".format(self._name, len(self._items))


class AsyncFolder(Folder):

    @createLock
    def __init__(self, name):
        super(AsyncFolder, self).__init__(name, None)
        self.async = True

    @injectLock
    def items(self, callback=None, lock=None):
        with lock:
            items = self._items
        if items:
            if callback:
                callback(items, None)
            return items
        else:
            if callback:
                return self._loadItemsAsync(callback)
            else:
                return self._loadItemsSync()

    def _loadItemsAsync(self, callback):
        def run():
            try:
                callback(self._loadItemsSync(), None)
            except Exception as e:
                callback([], e)
        worker.run(run)

    @injectLock
    def _loadItemsSync(self, lock):
        items = self._loadItems()
        with lock:
            self._items = items
        return items

    def _loadItems(self):
        return []


class _RetryAction(Action):

    def __init__(self, text, folder, callback):
        super(_RetryAction, self).__init__(text)
        self._folder = folder
        self._callback = callback

    def run(self, menu):
        self._folder.items(self._callback)


class _EmptyItem(Action):

    def __init__(self, text="<empty>"):
        super(_EmptyItem, self).__init__(text)


class _LoadingItem(Action):

    def __init__(self, text="Loading..."):
        super(_LoadingItem, self).__init__(text)


_LOADING_ITEM_INSTANCE = _LoadingItem()


class Menu(object):

    def __init__(self, root, showBackItem=True):
        self._root = root
        self._listeners = []
        self._menuStack = []
        if showBackItem:
            self._backItem = _BackItem()
        else:
            self._backItem = None
        self._emptyItem = _EmptyItem()
        self._loadingItem = _LOADING_ITEM_INSTANCE
        self._menuStackLock = RLock()
        self._folderLock = RLock()
        self._mainFolder = None
        self._currentFolder = None
        # self._currentItems
        # self._currentIndex
        self._setCurrentFolder(root)

    def _setCurrentFolder(self, folder, index=0):
        if getattr(folder, "async", False):
            self._setCurrentFolderAsynchron(folder, index)
        else:
            self._setCurrentFolderSynchron(folder, index)

    def _setCurrentFolderSynchron(self, folder, index):
        newItems = None
        try:
            newItems = folder.items()
        except Exception as e:
            text = "Opening Folder \"{0}\" failed".format(folder.name())
            logging.exception(text)
        if newItems is not None:
            with self._folderLock:
                self._setCurrentFolderAndStoreMainFolder(folder)
                self._updateItemsForFolder(folder, newItems, index, False)

    def _setCurrentFolderAsynchron(self, folder, index):
        def callback(newItems, error):
            if error:
                text = "Opening Folder \"{0}\" failed".format(folder.name())
                logging.exception(text)
                errorAction = _RetryAction("Error - Try again?", folder, callback)
                self._updateItemsForFolder(folder, [errorAction], 0, True)
            else:
                self._updateItemsForFolder(folder, newItems, index, True)
        with self._folderLock:
            self._setCurrentFolderAndStoreMainFolder(folder)
            self._updateItemsForFolder(folder, [self._loadingItem], 0, False)
        folder.items(callback)

    def _setCurrentFolderAndStoreMainFolder(self, folder):
        with self._folderLock:
            if self._currentFolder is not folder:
                if self.isRoot():
                    self._mainFolder = folder
                self._currentFolder = folder
                if self.isRoot():
                    self._mainFolder = None

    def _updateItemsForFolder(self, folder, items, index, notify):
        if isinstance(items, list):
            with self._folderLock:
                if self._currentFolder is not folder:
                    return
                self._currentItems = items
                if 0 < index >= len(self._currentItems):
                    self._currentIndex = len(self._currentItems) - 1
                else:
                    self._currentIndex = index
            if notify:
                self._fireAsyncCallback(event="update")
        else:
            text = "Opening Folder \"{0}\" failed, returned items should be of type list".format(folder.name())
            logging.error(text)

    def moveBy(self, offset):
        with self._folderLock:
            length = len(self._currentItems)
            if self._backItem is not None:
                length += 1
            if length > 0:
                self._currentIndex = (self._currentIndex + offset) % length
        return self

    def select(self):
        with self._folderLock:
            length = len(self._currentItems)
            if self._currentIndex == length and self._backItem is not None:
                entry = self._backItem
            else:
                if self._currentIndex < length:
                    entry = self._currentItems[self._currentIndex]
                else:
                    return self

        if hasattr(entry.__class__, "run") and callable(getattr(entry.__class__, "run")):
            try:
                entry.run(self)
            except Exception as e:
                text = "Action \"{0}\" executed with error".format(entry.name())
                logging.exception(text)
            return self
        else:
            with self._menuStackLock:
                stackTuple = (self._currentFolder, self._currentIndex)
                self._menuStack.append(stackTuple)
            self._setCurrentFolder(entry)
            return self

    def back(self):
        parent = None
        with self._menuStackLock:
            if len(self._menuStack) > 0:
                parent = self._menuStack.pop()
        if parent is not None:
            self._setCurrentFolder(parent[0], parent[1])
        return self

    def reset(self):
        with self._menuStackLock:
            self._menuStack = []  # self.menuStack.clear()
        self._setCurrentFolder(self._root)
        return self

    def folder(self):
        with self._folderLock:
            return self._currentFolder

    def item(self):
        with self._folderLock:
            length = len(self._currentItems)
            if self._currentIndex >= length and self._backItem is not None:
                return self._backItem
            elif length > 0:
                return self._currentItems[self._currentIndex]
            return self._emptyItem

    def isRoot(self):
        with self._folderLock:
            return self._root == self._currentFolder

    def mainFolder(self):
        with self._folderLock:
            return self._mainFolder

    def addListener(self, listener):  # not thread-safe yet
        self._listeners.append(listener)

    def _fireAsyncCallback(self, event):
        for listener in self._listeners:
            listener(self, event)
