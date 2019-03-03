class MenuState(object):

    def __init__(self, item, folder, index, items, mainFolder):
        self.item = item
        self.folder = folder
        self.items = items
        self.index = index
        self.mainFolder = mainFolder


class Menu(object):

    def __init__(self, rootFolder):
        self._rootFolder = rootFolder
        self._currentFolder = rootFolder
        self._currentFolderItems = []
        self._currentIndex = 0
        self._menuStack = []
        # TODO remove - can be determined from menu stack as well
        self._mainFolder = rootFolder

    def enterFolder(self, folder, items=[], index=0):
        stackTuple = (self._currentFolder, self._currentIndex)
        self._menuStack.append(stackTuple)
        self._setCurrentFolder(folder, items, index)

    def exitFolder(self):
        parent = None
        if len(self._menuStack) > 0:
            parent = self._menuStack.pop()
        if parent is not None:
            folder = parent[0]
            self._setCurrentFolder(folder)
            return {"folder": folder, "index": parent[1]}

    def _setCurrentFolder(self, folder, items=[], index=0):
        if self.isRoot():
            self._mainFolder = folder
        self._currentFolder = folder
        if self.isRoot():
            self._mainFolder = self._rootFolder
        self._currentFolderItems = items
        self._setCurrentIndex(index)

    def _setCurrentIndex(self, index):
        if 0 < index >= len(self._currentFolderItems):
            self._currentIndex = len(self._currentFolderItems) - 1
        else:
            self._currentIndex = index

    def moveCurrentIndex(self, offset):
        length = len(self._currentFolderItems)
        # if self._backItem is not None:
        #     length += 1
        if length > 0:
            self._currentIndex = (self._currentIndex + offset) % length

    def setCurrentItems(self, folder, items, index):
        if folder is self._currentFolder:
            self._currentFolderItems = items
            self._setCurrentIndex(index)

    def createMenuState(self):
        if self._currentIndex < len(self._currentFolderItems):
            currentItem = self._currentFolderItems[self._currentIndex]
        else:
            currentItem = None
        return MenuState(currentItem, \
            self._currentFolder, \
            self._currentIndex, \
            self._currentFolderItems, \
            self._mainFolder)

    def isRoot(self):
        return self._rootFolder == self._currentFolder
