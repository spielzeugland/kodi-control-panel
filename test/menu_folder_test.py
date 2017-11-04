import context
import mocks
from menu import Folder, CountingFolder


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


def test_lt_shouldBeFalse_forLowerCase():
    assert not Folder("a") < Folder("A")


def test_lt_shouldBeTrue_ignoring_case():
    assert Folder("a") < Folder("B")


def test_CountingFolder_withNoItems():
    f = CountingFolder("someName", [])
    assert f.name() == "someName (0)"


def test_CountingFolder_withOneItem():
    f = CountingFolder("someName", [Folder("a")])
    assert f.name() == "someName (1)"


def test_CountingFolder_withTwoItems():
    f = CountingFolder("someName", [Folder("a"), Folder("b")])
    assert f.name() == "someName (2)"
