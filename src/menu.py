from threading import Thread, RLock
from synchronized import createLock, withLock


class Action(object):

    def __init__(self, name):
        self._name = name

    def name(self):
        return self._name

    def run(self, menu):
        pass


class BackItem(Action):

    def __init__(self, name=".."):
        super(BackItem, self).__init__(name)

    def run(self, menu):
        menu.back()


class AsyncAction(Action):

    @createLock
    def __init__(self, name):
        super(AsyncAction, self).__init__(name)
        self._thread = None

    def run(self, menu):
        if not self._isRunning():
            self._scheduleRun()

    @withLock
    def _scheduleRun(self):
        self._thread = Thread(target=self._asyncRun)
        self._thread.setDaemon(True)
        self._thread.start()

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


class DynamicFolder(Folder):

    @createLock
    def __init__(self, name):
        super(DynamicFolder, self).__init__(name, None)
        self.async = True

    @withLock
    def items(self, callback=None):
        if self._items is not None:
            if callback:
                callback(self._items)
            return self._items
        else:
            if callback:
                self._loadItemsAsync(callback)
                return
            else:
                self._items = self._loadItems()
                return self._items

    def _loadItemsAsync(self, callback):
        def run():
            self._items = self._loadItemsWithLock()
            callback(self._items)
        thread = Thread(target=run)
        thread.setDaemon(True)
        thread.start()

    @withLock
    def _loadItemsWithLock(self):
        return self._loadItems()

    def _loadItems(self):
        return []


class _EmptyItem(Action):

    def __init__(self, text="<empty>"):
        super(_EmptyItem, self).__init__(text)


class _LoadingItem(Action):

    def __init__(self, text="Loading..."):
        super(_LoadingItem, self).__init__(text)


class Menu(object):

    def __init__(self, root, backItem=None):
        self._root = root
        self._menuStack = []
        self._backItem = backItem
        self._emptyItem = _EmptyItem()
        self._loadingItem = _LoadingItem()
        self._menuStackLock = RLock()
        self._folderLock = RLock()
        self._setCurrentFolder(root)
        # self._currentFolder
        # self._currentItems
        # self._currentIndex

    def _setCurrentFolder(self, folder, index=0):
        if getattr(folder, "async", False):
            self._setCurrentFolderAsynchron(folder, index)
        else:
            self._setCurrentFolderSynchron(folder, folder.items(), index)

    def _setCurrentFolderSynchron(self, folder, newItems, index):
        with self._folderLock:
            self._currentFolder = folder
            self._updateItemsForFolder(folder, newItems, index)

    def _setCurrentFolderAsynchron(self, folder, index):
        with self._folderLock:
            self._currentFolder = folder
            self._updateItemsForFolder(folder, [self._loadingItem])
        folder.items(lambda newItems: self._updateItemsForFolder(folder, newItems, index))

    def _updateItemsForFolder(self, folder, items, index=0):
        with self._folderLock:
            if self._currentFolder is not folder:
                return
            # TODO check type of items to be a list
            self._currentItems = items
            if index >= len(self._currentItems):
                self._currentIndex = len(self._currentItems) - 1
            else:
                self._currentIndex = index

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
                entry = self._currentItems[self._currentIndex]

        if hasattr(entry.__class__, "run") and callable(getattr(entry.__class__, "run")):
            # TODO error handling
            entry.run(self)
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
            if self._currentIndex == length and self._backItem is not None:
                return self._backItem
            elif length > 0:
                return self._currentItems[self._currentIndex]
            return self._emptyItem

    def isRoot(self):
        with self._folderLock:
            return self._root == self._currentFolder
