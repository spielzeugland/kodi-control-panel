import context
import mocks
from menu import Action, _BackItem


def test_run_shouldCallBackOnMenu():
    menu = mocks.Menu()
    _BackItem().run(menu)
    assert menu.backCnt == 1


def test_shouldBeAnAction():
    assert isinstance(_BackItem(), Action)


def test_init_shouldTakeName():
    assert _BackItem("myName").name() == "myName"


def test_init_shouldUseDefaultName():
    assert _BackItem().name() == ".."
