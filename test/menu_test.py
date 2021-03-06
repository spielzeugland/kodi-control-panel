import context
import mocks
from menu import Menu, Action, Folder, _BackItem, _RetryAction


folder1a = mocks.Folder("F1a", [])
folder1b = mocks.Folder("F1b", [])
folder1 = mocks.Folder("F1", [folder1a, folder1b])
folder2a = mocks.Folder("F2a", [])
folder2b = mocks.Folder("F2b", [])
folder2 = mocks.Folder("F2", [folder2a, folder2b])
a1 = mocks.Action("A1")
a2 = mocks.Action("A2")
a3 = mocks.Action("A3")
folder3 = mocks.Folder("Folder", [a1, a2, a3])
mainFolder = mocks.Folder("Nested", [folder1, folder2, folder3])
emptyFolder = mocks.Folder("Folder with no entries", [])


def test_init():
    menu = Menu(mainFolder)
    assert menu.folder() is mainFolder
    assert menu.item() is folder1
    assert menu.isRoot() is True


def test_moveBy0_shouldDoNothing():
    menu = Menu(mainFolder, showBackItem=False)
    menu.moveBy(0)
    assert menu.item() is folder1


def test_moveBy1():
    menu = Menu(mainFolder, showBackItem=False)
    menu.moveBy(1)
    assert menu.item() is folder2


def test_moveBy2():
    menu = Menu(mainFolder, showBackItem=False)
    menu.moveBy(2)
    assert menu.item() is folder3


def test_moveBy_overflow_withoutBackItem():
    menu = Menu(mainFolder, showBackItem=False)
    menu.moveBy(4)
    assert menu.item() is folder2


def test_moveByMinus1_withoutBackItem():
    menu = Menu(mainFolder, showBackItem=False)
    menu.moveBy(-1)
    assert menu.item() is folder3


def test_moveDoesNotChangeTheFolder():
    menu = Menu(mainFolder)
    menu.moveBy(1)
    assert menu.folder() is mainFolder
    assert menu.isRoot() is True


def test_moveBy0_withBackItem_shouldDoNothing():
    menu = Menu(mainFolder)
    menu.moveBy(0)
    assert menu.item() is folder1


def test_moveBy1_withBackItem():
    menu = Menu(mainFolder)
    menu.moveBy(1)
    assert menu.item() is folder2


def test_moveBy3_withBackItem():
    menu = Menu(mainFolder)
    menu.moveBy(3)
    assert menu.item() is menu._backItem


def test_moveBy_overflow_withBackItem():
    menu = Menu(mainFolder)
    menu.moveBy(4)
    assert menu.item() is folder1


def test_moveByMinus1_withBackItem():
    menu = Menu(mainFolder)
    menu.moveBy(-1)
    assert menu.item() is menu._backItem


def test_moveByMinus2_withBackItem():
    menu = Menu(mainFolder)
    menu.moveBy(-2)
    assert menu.item() is folder3


def test_moveBy1_shouldNotFailForEmptyFolder():
    menu = Menu(emptyFolder, showBackItem=False)
    menu.moveBy(1)
    assert menu.item() is menu._emptyItem


def test_moveBy0_shouldNotFailForEmptyFolder():
    menu = Menu(emptyFolder, showBackItem=False)
    menu.moveBy(0)
    assert menu.item() is menu._emptyItem


def test_moveByMinus1_shouldNotFailForEmptyFolder():
    menu = Menu(emptyFolder, showBackItem=False)
    menu.moveBy(-1)
    assert menu.item() is menu._emptyItem


def test_moveBy1_withBackItem_shouldNotFailForEmptyFolder():
    menu = Menu(emptyFolder)
    menu.moveBy(1)
    assert menu.item() is menu._backItem


def test_moveBy0_withBackItem_shouldNotFailForEmptyFolder():
    menu = Menu(emptyFolder)
    menu.moveBy(0)
    assert menu.item() is menu._backItem


def test_moveByMinus1_withBackItem_shouldNotFailForEmptyFolder():
    menu = Menu(emptyFolder)
    menu.moveBy(-1)
    assert menu.item() is menu._backItem


def test_select_shouldExecuteSelectedAction():
    action = mocks.Action("Action")
    folder = mocks.Folder("Folder", [action])
    menu = Menu(folder)
    menu.select()
    assert action.runCnt == 1


def test_select_shouldAddMessageForFailingAction():
    someException = Exception("exception text")
    action = mocks.FailingAction("My Failing Action", someException)
    folder = mocks.Folder("Folder", [action])
    menu = Menu(folder)
    menu.select()
    # TODO assert message


def test_select_shouldAddMessageForFailingFolder():
    someException = Exception("exception text")
    failingFolder = mocks.FailingFolder("my failing folder", someException)
    folder = mocks.Folder("Folder", [failingFolder])
    menu = Menu(folder)
    menu.select()
    # TODO assert message


def test_select_shouldAddMessageForFolderReturningInvalidItems():
    failingFolder = mocks.IncorrectFolder("my incorrect folder")
    folder = mocks.Folder("Folder", [failingFolder])
    menu = Menu(folder)
    menu.select()
    # TODO assert message


def test_select_shouldOpenFolder():
    menu = Menu(mainFolder)
    menu.select()
    assert menu.folder() is folder1


def test_select_shouldLeaveRootFolder():
    menu = Menu(mainFolder)
    menu.select()
    assert menu.isRoot() is False


def test_select_shouldOpenFolderAndShowItsFirstEntry():
    menu = Menu(mainFolder)
    menu.moveBy(1)
    menu.select()
    assert menu.folder() is folder2
    assert menu.item() is folder2a


def test_select_multiLevel():
    menu = Menu(mainFolder)
    menu.moveBy(1).select().moveBy(1).select()
    assert menu.folder() is folder2b


def test_select_emptyFolder_shouldDoNothing():
    menu = Menu(emptyFolder, showBackItem=False)
    assert menu.item() is menu._emptyItem
    menu.select()
    assert menu.item() is menu._emptyItem


def test_withBackItem_shouldShowBackItemInEmptyFolder():
    menu = Menu(emptyFolder)
    assert menu.item() is menu._backItem


def test_back():
    menu = Menu(mainFolder)
    menu.select()
    menu.back()
    assert menu.folder() is mainFolder


def test_back_shouldRememberIndex():
    menu = Menu(mainFolder)
    menu.moveBy(1)
    menu.select()
    menu.back()
    assert menu.item() is folder2


def test_back_shouldDoNothingForRootFolder():
    menu = Menu(mainFolder)
    menu.back().back()
    assert menu.folder() is mainFolder


def test_back_doesNotNotifyListenersIfFolderNotChanged():
    countingListener = mocks.CountingMenuListener()
    menu = Menu(mainFolder)
    menu.addListener(countingListener)
    menu.back()
    assert len(countingListener.calls) == 0


def test_back_multiLevel():
    menu = Menu(mainFolder)
    menu.moveBy(1).select().moveBy(1).select()
    menu.back()
    assert menu.folder() is folder2
    assert menu.item() is folder2b
    menu.back()
    assert menu.folder() is mainFolder
    assert menu.item() is folder2


def test_back_shouldGoToLastElementIfParentItemListWasShortended_withoutBackItem():
    subFolders = [Folder("a", []), Folder("b", []), Folder("c", [])]
    folder = Folder("", subFolders)
    menu = Menu(folder, showBackItem=False)
    menu.moveBy(-1).select()
    subFolders.pop()
    menu.back()
    assert menu.item() is subFolders[1]


def test_back_shouldGoToLastElementIfParentItemListWasShortended_withBackItem():
    subFolders = [Folder("a", []), Folder("b", []), Folder("c", [])]
    folder = Folder("", subFolders)
    menu = Menu(folder)
    menu.moveBy(-1).select()
    subFolders.pop()
    menu.back()
    assert menu.item() is menu._backItem


def test_reset_shouldGoToFirstItemOfMainFolder():
    menu = Menu(mainFolder)
    menu.moveBy(1).select().moveBy(1).select()
    menu.reset()
    assert menu.folder() is mainFolder
    assert menu.item() is folder1
    assert len(menu._menuStack) == 0


def test_select_shouldLoadAsyncFolders():
    asyncFolder = mocks.SynchronAsyncFolder("Dynamic", [])
    dynamicMainFolder = mocks.Folder("Main", [asyncFolder])
    menu = Menu(dynamicMainFolder)
    menu.select()
    assert asyncFolder.loadItemsCnt == 1
    assert menu._currentItems == asyncFolder._itemsToLoad


def test_select_shouldShowLoadingWhileGettingItemsAsynchronously():
    asyncFolder = mocks.NeverLoadingFolder("Dynamic", [])
    dynamicMainFolder = mocks.Folder("Main", [asyncFolder])
    menu = Menu(dynamicMainFolder)
    menu.select()
    assert asyncFolder.loadItemsCnt == 0
    assert menu.item() is menu._loadingItem


def test_select_shouldShowRetryActionWhenLoadingFolderFailed_Asynchronously():
    asyncFolder = mocks.FailingSynchronAsyncFolder("Dynamic", Exception(""))
    dynamicMainFolder = mocks.Folder("Main", [asyncFolder])
    menu = Menu(dynamicMainFolder)
    menu.select()
    assert isinstance(menu.item(), _RetryAction)


def test_updateItemsForFolder_shouldDoNothingForDifferentFolder():
    menu = Menu(mainFolder)
    menu._updateItemsForFolder(folder2, folder2.items(), 0, False)
    assert menu.folder() is mainFolder
    assert menu.item() is folder1


def test_updateItemsForFolder_shouldCallHandler():
    countingListener = mocks.CountingMenuListener()
    menu = Menu(mainFolder)
    menu.addListener(countingListener.handler)
    menu._updateItemsForFolder(mainFolder, mainFolder.items(), 0, True)
    assert len(countingListener.calls) == 1


def test_updateItemsForFolder_shouldNotCallHandler():
    countingListener = mocks.CountingMenuListener()
    menu = Menu(mainFolder)
    menu.addListener(countingListener.handler)
    menu._updateItemsForFolder(mainFolder, mainFolder.items(), 0, False)
    assert len(countingListener.calls) == 0


def test_mainFolder_shouldReturnNoneInRootFolder():
    menu = Menu(mainFolder)
    assert menu.mainFolder() is None


def test_mainFolder_shouldReturnCurrentMainFolder():
    menu = Menu(mainFolder)
    menu.select()
    assert menu.folder() is folder1
    assert menu.mainFolder() is folder1
    menu.select()
    assert menu.folder() is folder1a
    assert menu.mainFolder() is folder1
    menu.back().back()
    assert menu.mainFolder() is None
