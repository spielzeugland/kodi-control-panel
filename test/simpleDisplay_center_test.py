import context
import simpleDisplay as s


def test_center_4spacesLeft():
    assert s._center("abc", 7) == "  abc  "


def test_center_2spacesleft():
    assert s._center("abc", 5) == " abc "


def test_center_5spacesLeft():
    assert s._center("abc", 8) == "  abc   "


def test_center_1spaceLeft():
    assert s._center("abc", 4) == "abc "


def test_center_shouldDoNothingForEqualTextLength():
    assert s._center("abc", 3) == "abc"


def test_center__shouldDoNothingForLongerText():
    assert s._center("abcdef", 4) == "abcdef"
