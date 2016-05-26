import context
import mocks
from src.menu import Menu

staticAction = mocks.Action("Static Action") 
staticFolder = mocks.Folder("Static", [staticAction])
staticMainFolder = mocks.Folder("Main", [staticFolder])

dynamicAction = mocks.Action("Dynamic Action")
dynamicFolder = mocks.DynamicFolder("Dynamic", [dynamicAction])
dynamicMainFolder = mocks.Folder("Main", [dynamicFolder])
backItem = mocks.Action("<Back>")

def test_shouldNotCallLoaderForStaticFolders():
	loader = mocks.SynchronItemLoader
	menu = Menu(staticMainFolder, backItem, loader)
	menu.select()
	assert len(loader.loadItemsStack) == 0

def test_shouldCallLoaderForDynamicFolders():
	loader = mocks.SynchronItemLoader
	menu = Menu(dynamicMainFolder, backItem, loader)
	menu.select()
	assert len(loader.loadItemsStack) == 1
	assert loader.loadItemsStack[0] is dynamicFolder

def test_shouldShowLoadingWhileGettingItemsAsynchronously():
	loader = mocks.NeverItemLoader
	menu = Menu(dynamicMainFolder, backItem, loader)
	menu.select()
	assert menu.item() is menu._loadingItem

def test_updateItemsForFolderShouldDoNothingForDifferentFolder():
	menu = Menu(staticMainFolder, backItem)
	menu._updateItemsForFolder(dynamicMainFolder, [dynamicAction])
	assert menu.folder() is staticMainFolder
	assert menu.item() is staticFolder

