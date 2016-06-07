import context
import mocks
from src.menu import Menu

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

