import context
import mocks
from src.controller import BackItem
import menu

def test_shouldBeSubClassOfMenuBackItem():
    assert isinstance(BackItem(), menu.BackItem)

def test_initShouldTakeName():
    backItem = BackItem("myName")
    assert backItem.name() == "myName"

def test_runShouldCallMenuIfControllerIsNotSet():
    menu = mocks.Menu()
    backItem = BackItem()
    backItem.run(menu)
    assert menu.backCnt == 1

def test_runShouldCallExitMenuModeOnController():
    menu = mocks.Menu(isRoot=True)
    controller = mocks.Controller()
    backItem = BackItem()
    backItem.controller = controller
    backItem.run(menu)
    assert controller.exitMenuModeCnt == 1
    assert menu.backCnt == 0

def test_runShouldNotCallExitMenuModeOnController():
    menu = mocks.Menu(isRoot=False)
    controller = mocks.Controller()
    backItem = BackItem()
    backItem.controller = controller
    backItem.run(menu)
    assert controller.exitMenuModeCnt == 0
    assert menu.backCnt == 1