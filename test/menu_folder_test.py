import context
import mocks
from menu import Folder


def test_init_shouldTakeName():
    assert Folder("myName").name() == "myName"


def test_init_shouldTakeItem():
    items = []
    folder = Folder("", items)
    assert folder.items() == items


def test_init_shouldUseDefaultItems():
    items = []
    folder = Folder("")
    assert len(folder.items()) == 0


def test_lt_shouldBeTrue():
    assert Folder("abc") < Folder("abd")


def test_lt_shouldBeFalse():
    assert not Folder("def") < Folder("abc")


def test_lt_shouldBeFalse_forEqualName():
    assert not Folder("abc") < Folder("abc")
