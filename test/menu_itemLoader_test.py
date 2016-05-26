import context
import mocks
from src.menu import _ItemLoader, _LoadingItem
from time import sleep

dynamicAction1 = mocks.Action("Dynamic Action 1")
dynamicAction2 = mocks.Action("Dynamic Action 2")

def test_loadItemsShouldCallBackToMenuWhenItemsAreLoaded():
	dynamicFolder = mocks.DynamicFolder("Dynamic", [dynamicAction1, dynamicAction2])
	menu = mocks.Menu()
	loader = _ItemLoader()
	loader.loadItems(menu, dynamicFolder)
	sleep(0.3)
	assert len(menu.updateItemsStack) == 1
	assert menu.updateItemsStack[0][0] is dynamicFolder
	assert menu.updateItemsStack[0][1][0] is dynamicAction1
	assert menu.updateItemsStack[0][1][1] is dynamicAction2
	
def test_loadItemsShouldResetCurrentItemIndex():
	dynamicFolder = mocks.DynamicFolder("Dynamic", [dynamicAction1, dynamicAction2])
	menu = mocks.Menu()
	loader = _ItemLoader()
	loader.loadItems(menu, dynamicFolder)
	sleep(0.3)
	assert menu.updateItemsStack[0][2] is 0
