import context
import simpleDisplay as s


def test_sanitize_shouldRemoveLineBreaks():
    assert s._sanitize("ab\ncd") == "ab cd"
