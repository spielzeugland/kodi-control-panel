from time import sleep
import context
import mocks
import messages
from menu import Folder, DynamicFolder


class DynamicFolderForTest(DynamicFolder):

    def __init__(self, name, items, delay=0):
        super(DynamicFolderForTest, self).__init__(name)
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

    def handler(self, items):
        self.calls.append(items)


expectedItems = ["abc", "def"]


def test_shouldBeSubClassOfFolder():
    assert isinstance(DynamicFolder(""), Folder)


def test_init_shouldTakeName():
    folder = DynamicFolder("myName")
    assert folder.name() == "myName"


def test_loadItemsShouldReturnEmptyList():
    folder = DynamicFolder("")
    assert len(folder._loadItems()) == 0


def test_shouldBeAsync():
    folder = DynamicFolderForTest("name", expectedItems)
    assert folder.async is True


def test_items_withoutCallback_shouldBeSynchron():
    folder = DynamicFolderForTest("name", expectedItems)
    items = folder.items()
    assert items == expectedItems
    assert folder.loadItemsCnt == 1


def test_items_withCallback_shouldReturnNone():
    callback = CountingCallback()
    folder = DynamicFolderForTest("name", expectedItems)
    items = folder.items(callback.handler)
    assert items is None


def test_items_withCallback_shouldBeAsynchron():
    callback = CountingCallback()
    folder = DynamicFolderForTest("name", expectedItems, 0.1)
    items = folder.items(callback.handler)
    assert folder.loadItemsCnt == 0
    sleep(0.2)
    assert folder.loadItemsCnt == 1
    assert callback.calls[0] == expectedItems


def test_items_withoutCallback_shouldReturnCachedItemsWhenCallingSecondTime():
    folder = DynamicFolderForTest("name", expectedItems)
    items = folder.items()
    folder.loadItemsCnt = 0  # reseting counter
    items = folder.items()
    assert items == expectedItems
    assert folder.loadItemsCnt == 0


def test_items_withCallback_shouldReturnCachedItemsWhenCallingSecondTime():
    folder = DynamicFolderForTest("name", expectedItems, 0.2)
    items = folder.items()
    folder.loadItemsCnt = 0  # reseting counter
    callback = CountingCallback()
    items = folder.items(callback.handler)
    assert items == expectedItems
    assert folder.loadItemsCnt == 0
    assert callback.calls[0] == expectedItems


def test_runAsyncShouldAddMessageInCaseOfError():
    messages._clear()
    someException = Exception("the exception message")
    folder = mocks.FailingDynamicFolder("my failing folder", someException)
    folder._loadItemsWithoutLock()
    newMessages = messages.getUnread()
    assert len(newMessages) is 1
    assert newMessages[0].text == "Folder \"my failing folder\" could not be loaded"
    assert newMessages[0].details is None
    assert newMessages[0].sysInfo[1] is someException
