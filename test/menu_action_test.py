import context
import mocks
import messages
from menu import Action


def test_init_shouldTakeName():
    assert Action("myName").name() == "myName"


def test_run_doesNothing():
    menu = mocks.Menu()
    Action("").run(menu)


def test_lt_shouldBeTrue():
    assert Action("abc") < Action("abd")


def test_lt_shouldBeFalse():
    assert not Action("def") < Action("abc")


def test_lt_shouldBeFalse_forEqualName():
    assert not Action("abc") < Action("abc")


def test_lt_shouldBeFalse_forLowerCase():
    assert not Action("a") < Action("A")


def test_lt_shouldBeTrue_ignoring_case():
    assert Action("a") < Action("B")
