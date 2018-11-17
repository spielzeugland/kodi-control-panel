from time import sleep
import context
import mocks
from menu import Folder, AsyncFolder, _RetryAction


class AsyncFolderForTest(AsyncFolder):

    def __init__(self, name, items, delay=0):
        super(AsyncFolderForTest, self).__init__(name)
        self._itemsToLoad = items
        self._delay = delay
        self.loadItemsCnt = 0

    def _loadItems(self):
        sleep(self._delay)
        self.loadItemsCnt += 1
        return self._itemsToLoad


class CountingCallback(object):

    def __init__(self):
        self.calls = []

    def handler(self, items, error):
        self.calls.append({"items": items, "error": error})


expectedItems = ["abc", "def"]


def test_shouldBeSubClassOfFolder():
    assert isinstance(AsyncFolder(""), Folder)


def test_init_shouldTakeName():
    folder = AsyncFolder("myName")
    assert folder.name() == "myName"


def test_loadItemsShouldReturnEmptyList():
    folder = AsyncFolder("")
    assert len(folder._loadItems()) == 0


def test_shouldBeAsync():
    folder = AsyncFolderForTest("name", expectedItems)
    assert folder.isAsync is True


def test_items_withoutCallback_shouldBeSynchron():
    folder = AsyncFolderForTest("name", expectedItems)
    items = folder.items()
    assert items == expectedItems
    assert folder.loadItemsCnt == 1


def test_items_withCallback_shouldReturnNone():
    callback = CountingCallback()
    folder = AsyncFolderForTest("name", expectedItems)
    items = folder.items(callback.handler)
    assert items is None


def test_items_withCallback_shouldBeAsynchron():
    callback = CountingCallback()
    folder = AsyncFolderForTest("name", expectedItems, 0.1)
    items = folder.items(callback.handler)
    assert folder.loadItemsCnt == 0
    sleep(0.2)
    assert folder.loadItemsCnt == 1
    assert callback.calls[0]["items"] == expectedItems
    assert callback.calls[0]["error"] is None


def test_items_withoutCallback_shouldReturnCachedItemsWhenCallingSecondTime():
    folder = AsyncFolderForTest("name", expectedItems)
    folder.items()
    folder.loadItemsCnt = 0  # reseting counter
    items = folder.items()
    assert items == expectedItems
    assert folder.loadItemsCnt == 0


def test_items_withCallback_shouldForwardError():
    callback = CountingCallback()
    e = Exception("Some Exception")
    folder = mocks.FailingSynchronAsyncFolder("name", e)
    items = folder.items(callback.handler)
    assert callback.calls[0]["error"] is e
    assert len(callback.calls[0]["items"]) == 0


def test_items_withCallback_shouldReturnCachedItemsWhenCallingSecondTime():
    folder = AsyncFolderForTest("name", expectedItems, 0.2)
    folder.items()
    folder.loadItemsCnt = 0  # reseting counter
    callback = CountingCallback()
    items = folder.items(callback.handler)
    assert items == expectedItems
    assert folder.loadItemsCnt == 0
    assert callback.calls[0]["items"] == expectedItems
