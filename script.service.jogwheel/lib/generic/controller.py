from timer import ExtensibleTimer as Timer
from synchronized import createLock, withLock
from menu import Menu
from menu_old import _LoadingItem
import worker


_LOADING_ITEM_INSTANCE = _LoadingItem()


class Mode(object):
    Player = 0
    Menu = 1


class Controller(object):

    @createLock
    def __init__(self, player, rootFolder, listener):
        self._player = player
        self._listener = listener
        self._menu = Menu(rootFolder)
        self._loadingItem = _LOADING_ITEM_INSTANCE
        self._timer = Timer(lambda: self._exitMenuMode())
        # load first level initially 
        self._menu.enterFolder(rootFolder, [self._loadingItem])
        self._loadFolder(rootFolder)

    @withLock
    def moveBy(self, offset):
        if self._timer.start():
            self._menu.moveCurrentIndex(offset)
        self._updateView()

    @withLock
    def click(self, item):
        if self._timer.start():
            if item is not None:
                if hasattr(item.__class__, "run") and callable(getattr(item.__class__, "run")):
                    self._runAction(item)
                else:
                    self._menu.enterFolder(item, [self._loadingItem])
                    self._loadFolder(item)
        self._updateView()

    @withLock
    def longClick(self):
        if self._timer.start():
            info = self._menu.exitFolder()
            if info is not None:
                self._loadFolder(info["folder"], info["index"])
        self._updateView()

    @withLock
    def _updateView(self):
        if self._timer.isRunning():
            self._listener({
                "mode": Mode.Menu,
                "state": self._menu.createMenuState()
            })
        else:
            self._listener({
                "mode": Mode.Player,
                "state": self._player
            })

    @withLock
    def _runAction(self, action):
        def task():
            # TODO error handling
            action.run()
        worker.run(task)

    @withLock
    def _loadFolder(self, folder, index=0):
        def task():
            try:
                # TODO error handling
                items = folder.items()
                self._handleFolderLoaded(folder, items, index)
            except Exception as e:
                print(e)
        worker.run(task)

    @withLock
    def _handleFolderLoaded(self, folder, items, index):
        self._menu.setCurrentItems(folder, items, index) 
        if self._timer.isRunning():
            print("update view")
            self._timer.start()
            self._updateView()

    @withLock
    def _mode(self):
        if self._timer.isRunning():
            return Mode.Menu
        else:
            return Mode.Player

    @withLock
    def _exitMenuMode(self):
        self._timer.cancel()
        self._updateView()
