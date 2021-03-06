import os
import pycodestyle


def _checkCodeStyle(folder):
    source_files = []
    source_path = os.path.abspath(folder)
    for root, directories, filenames in os.walk(source_path):
        toAdd = [os.path.join(root, f) for f in filenames if f.endswith(".py") and not f.endswith("create_gpio_user_permission.py")]
        source_files.extend(toAdd)
    style = pycodestyle.StyleGuide(quiet=False, max_line_length=140)
    result = style.check_files(source_files)
    assert result.total_errors == 0


def test_sourceCodeShouldFollowPep8Ccodestyle():
    _checkCodeStyle("./script.service.jogwheel")


def test_samplesCodeShouldFollowPep8Ccodestyle():
    _checkCodeStyle("./samples")


def test_testCodeShouldFollowPep8Ccodestyle():
    _checkCodeStyle("./test")
