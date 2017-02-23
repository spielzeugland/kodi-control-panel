import context
import mocks
import messages
from menu import Menu, Action, Folder, BackItem


backItem = mocks.Action("<Back>")
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
    menu = Menu(mainFolder)
    menu.moveBy(0)
    assert menu.item() is folder1


def test_moveBy1():
    menu = Menu(mainFolder)
    menu.moveBy(1)
    assert menu.item() is folder2


def test_moveBy3():
    menu = Menu(mainFolder)
    menu.moveBy(3)
    assert menu.item() is folder1


def test_moveBy4():
    menu = Menu(mainFolder)
    menu.moveBy(4)
    assert menu.item() is folder2


def test_moveByMinus1():
    menu = Menu(mainFolder)
    menu.moveBy(-1)
    assert menu.item() is folder3


def test_moveDoesNotChangeTheFolder():
    menu = Menu(mainFolder)
    menu.moveBy(1)
    assert menu.folder() is mainFolder
    assert menu.isRoot() is True


def test_moveBy0_withBackItem_shouldDoNothing():
    menu = Menu(mainFolder, backItem)
    menu.moveBy(0)
    assert menu.item() is folder1


def test_moveBy1_withBackItem():
    menu = Menu(mainFolder, backItem)
    menu.moveBy(1)
    assert menu.item() is folder2


def test_moveBy3_withBackItem():
    menu = Menu(mainFolder, backItem)
    menu.moveBy(3)
    assert menu.item() is backItem


def test_moveBy4_withBackItem():
    menu = Menu(mainFolder, backItem)
    menu.moveBy(4)
    assert menu.item() is folder1


def test_moveByMinus1_withBackItem():
    menu = Menu(mainFolder, backItem)
    menu.moveBy(-1)
    assert menu.item() is backItem


def test_moveByMinus2_withBackItem():
    menu = Menu(mainFolder, backItem)
    menu.moveBy(-2)
    assert menu.item() is folder3


def test_moveBy1_shouldNotFailForEmptyFolder():
    menu = Menu(emptyFolder)
    menu.moveBy(1)
    assert menu.item() is menu._emptyItem


def test_moveBy0_shouldNotFailForEmptyFolder():
    menu = Menu(emptyFolder)
    menu.moveBy(0)
    assert menu.item() is menu._emptyItem


def test_moveByMinus1_shouldNotFailForEmptyFolder():
    menu = Menu(emptyFolder)
    menu.moveBy(-1)
    assert menu.item() is menu._emptyItem


def test_moveBy1_withBackItem_shouldNotFailForEmptyFolder():
    menu = Menu(emptyFolder, backItem)
    menu.moveBy(1)
    assert menu.item() is backItem


def test_moveBy0_withBackItem_shouldNotFailForEmptyFolder():
    menu = Menu(emptyFolder, backItem)
    menu.moveBy(0)
    assert menu.item() is backItem


def test_moveByMinus1_withBackItem_shouldNotFailForEmptyFolder():
    menu = Menu(emptyFolder, backItem)
    menu.moveBy(-1)
    assert menu.item() is backItem


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
    messages._clear()

    menu.select()
    newMessages = messages.getUnread()
    assert len(newMessages) == 1
    assert newMessages[0].text == "Action \"My Failing Action\" executed with error"
    assert newMessages[0].details is None
    assert newMessages[0].sysInfo[1] is someException


def test_select_shouldAddMessageForFailingFolder():
    someException = Exception("exception text")
    failingFolder = mocks.FailingFolder("my failing folder", someException)
    folder = mocks.Folder("Folder", [failingFolder])
    menu = Menu(folder)
    messages._clear()

    menu.select()
    newMessages = messages.getUnread()
    assert len(newMessages) is 1
    assert newMessages[0].text == "Folder \"my failing folder\" could not be loaded"
    assert newMessages[0].details is None
    assert newMessages[0].sysInfo[1] is someException


def test_select_shouldAddMessageForFolderReturningInvalidItems():
    failingFolder = mocks.IncorrectFolder("my incorrect folder")
    folder = mocks.Folder("Folder", [failingFolder])
    menu = Menu(folder)
    messages._clear()

    menu.select()
    newMessages = messages.getUnread()
    assert len(newMessages) is 1
    assert newMessages[0].text == "Folder \"my incorrect folder\" could not be loaded"
    assert newMessages[0].details == "Returned items object should be of type list"


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


def test_select_shouldExecuteBackItemIfSelected():
    menu = Menu(mainFolder, backItem)
    menu.moveBy(-1).select()
    assert backItem.runCnt == 1


def test_select_emptyFolder_shouldDoNothing():
    menu = Menu(emptyFolder)
    assert menu.item() is menu._emptyItem
    menu.select()
    assert menu.item() is menu._emptyItem


def test_withBackItem_shouldShowBackItemInEmptyFolder():
    menu = Menu(emptyFolder, backItem)
    assert menu.item() is backItem


def test_back():
    menu = Menu(mainFolder)
    menu.select()
    menu.back()
    assert menu.folder() is mainFolder


def test_back_shouldRemeberIndex():
    menu = Menu(mainFolder)
    menu.moveBy(1)
    menu.select()
    menu.back()
    assert menu.item() is folder2


def test_back_shouldDoNothingForRootFolder():
    menu = Menu(mainFolder)
    menu.back().back()
    assert menu.folder() is mainFolder


def test_back_multiLevel():
    menu = Menu(mainFolder)
    menu.moveBy(1).select().moveBy(1).select()
    menu.back()
    assert menu.folder() is folder2
    assert menu.item() is folder2b
    menu.back()
    assert menu.folder() is mainFolder
    assert menu.item() is folder2


def test_back_shouldGoToLastElementIfParentItemListWasShortended():
    subFolders = [Folder("a", []), Folder("b", []), Folder("c", [])]
    folder = Folder("", subFolders)
    menu = Menu(folder)
    menu.moveBy(-1).select()
    subFolders.pop()
    menu.back()
    assert menu.item() == subFolders[1]


def test_reset_shouldGoToFirstItemOfMainFolder():
    menu = Menu(mainFolder)
    menu.moveBy(1).select().moveBy(1).select()
    menu.reset()
    assert menu.folder() is mainFolder
    assert menu.item() is folder1
    assert len(menu._menuStack) == 0


def test_select_shouldLoadDynamicFolders():
    dynamicFolder = mocks.SynchronDynamicFolder("Dynamic", [])
    dynamicMainFolder = mocks.Folder("Main", [dynamicFolder])
    menu = Menu(dynamicMainFolder)
    menu.select()
    assert dynamicFolder.loadItemsCnt == 1
    assert menu._currentItems == dynamicFolder._itemsToLoad


def test_select_shouldShowLoadingWhileGettingItemsAsynchronously():
    dynamicFolder = mocks.NeverLoadingFolder("Dynamic", [])
    dynamicMainFolder = mocks.Folder("Main", [dynamicFolder])
    menu = Menu(dynamicMainFolder)
    menu.select()
    assert dynamicFolder.loadItemsCnt == 0
    assert menu.item() is menu._loadingItem


def test_updateItemsForFolder_shouldDoNothingForDifferentFolder():
    menu = Menu(mainFolder)
    menu._updateItemsForFolder(folder2, folder2.items())
    assert menu.folder() is mainFolder
    assert menu.item() is folder1


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


def test_Action_init_shouldTakeName():
    assert Action("myName").name() == "myName"


def test_Action_run_doesNothing():
    menu = mocks.Menu()
    Action("").run(menu)


def test_Folder_init_shouldTakeName():
    assert Folder("myName").name() == "myName"


def test_Folder_init_shouldTakeItem():
    items = []
    folder = Folder("", items)
    assert folder.items() == items


def test_Folder_init_shouldUseDefaultItems():
    items = []
    folder = Folder("")
    assert len(folder.items()) == 0


def test_BackItem_run_shouldCallBackOnMenu():
    menu = mocks.Menu()
    BackItem().run(menu)
    assert menu.backCnt == 1


def test_BackItem_shouldBeAnAction():
    assert isinstance(BackItem(), Action)


def test_BackItem_init_shouldTakeName():
    assert BackItem("myName").name() == "myName"


def test_BackItem_init_shouldUseDefaultName():
    assert BackItem().name() == ".."
