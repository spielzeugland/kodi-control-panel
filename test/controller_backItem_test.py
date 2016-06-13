import context
import mocks
from controller import BackItem
import menu


def test_shouldBeSubClassOfAction():
    assert isinstance(BackItem(), menu.Action)


def test_init_shouldUseDefaultName():
    backItem = BackItem()
    assert backItem.name() == ".."


def test_init_shouldTakeName():
    backItem = BackItem("myName")
    assert backItem.name() == "myName"


def test_run_shouldCallMenuIfControllerIsNotSet():
    menu = mocks.Menu()
    backItem = BackItem()
    backItem.run(menu)
    assert menu.backCnt == 1


def test_run_shouldCallExitMenuModeOnController():
    menu = mocks.Menu(isRoot=True)
    controller = mocks.Controller()
    backItem = BackItem()
    backItem.controller = controller
    backItem.run(menu)
    assert controller.exitMenuModeCnt == 1
    assert menu.backCnt == 0


def test_run_shouldNotCallExitMenuModeOnController():
    menu = mocks.Menu(isRoot=False)
    controller = mocks.Controller()
    backItem = BackItem()
    backItem.controller = controller
    backItem.run(menu)
    assert controller.exitMenuModeCnt == 0
    assert menu.backCnt == 1
