import context
import simpleDisplay as s


def test_oneLinePerfectFit():
    lines = s._asLines("ab", 4, 1)
    assert len(lines) == 1
    assert lines[0] == " ab "


def test_oneLine_showEllipsisIfTextTooLong():
    lines = s._asLines("abcdefghijklmnop", 10, 1)
    assert len(lines) == 1
    assert lines[0] == " abcde... "


def test_oneLine_shouldNotShowEllipsisIfNotEnoughSpace():
    lines = s._asLines("ab", 3, 1)
    assert len(lines) == 1
    assert lines[0] == " a "


def test_twoLines_perfectFit():
    lines = s._asLines("abcdefghijklmnop", 10, 2)
    assert len(lines) == 2
    assert lines[0] == " abcdefgh "
    assert lines[1] == " ijklmnop "


def test_twoLines_showEllipsisIfTextTooLong():
    lines = s._asLines("abcdefghijklmnopq", 10, 2)
    assert len(lines) == 2
    assert lines[0] == " abcdefgh "
    assert lines[1] == " ijklm... "


def test_twoLines_shouldNotShowEllipsisIfNotEnoughSpace():
    lines = s._asLines("abcdefghijklmnopqrstuvwxyz", 3, 2)
    assert len(lines) == 2
    assert lines[0] == " a "
    assert lines[1] == " b "


def test_shouldAddTrailingBlankLines():
    lines = s._asLines("abcd", 10, 2)
    assert len(lines) == 2
    assert lines[0] == " abcd     "
    assert lines[1] == "          "


def test_shouldAddLeadingAndTrailingBlankLines():
    lines = s._asLines("abcd", 10, 3)
    assert len(lines) == 3
    assert lines[0] == "          "
    assert lines[1] == " abcd     "
    assert lines[2] == "          "


def test_shouldAddTwoTrailingBlankLines():
    lines = s._asLines("abcdabcd", 20, 4)
    assert len(lines) == 4
    assert lines[0] == "                    "
    assert lines[1] == " abcdabcd           "
    assert lines[2] == "                    "
    assert lines[3] == "                    "


def test_shouldNotFailIfNoSpaceLeft():
    lines = s._asLines("abcdefghijklmnopqrstuvwxyz", 3, 2, 4)
    assert len(lines) == 2
    assert lines[0] == "   "
    assert lines[1] == "   "
