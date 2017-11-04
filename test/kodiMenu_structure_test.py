import context
import mocks
from kodiMenu import Default, Sorted, _Sorted, Grouped, _Grouped
import menu

someFolder = menu.Folder("some")
length = 1


def test_Default_constructor():
    Default(someFolder, length)


def test_Default_addOneItem():
    d = Default(someFolder, length)
    d.add("item1")
    items = d.asList()
    assert len(items) is 1
    assert items[0] is "item1"


def test_Default_addTwoItems():
    d = Default(someFolder, length)
    d.add("first item")
    d.add("second item")
    items = d.asList()
    assert len(items) is 2
    assert items[0] is "first item"
    assert items[1] is "second item"


def test_Default_shouldKeepInsertOrder():
    d = Default(someFolder, length)
    d.add("z")
    d.add("a")
    items = d.asList()
    assert len(items) is 2
    assert items[0] is "z"
    assert items[1] is "a"


def test_Sorted_factory_defaultArguments():
    constructor = Sorted()
    s = constructor(None, 0)
    assert isinstance(s, _Sorted)


def test_Sorted_factory_shouldReturnSortedIfSizeIsAboveMinSize():
    constructor = Sorted(5)
    s = constructor(someFolder, 10)
    assert isinstance(s, _Sorted)


def test_Sorted_factory_shouldReturnSortedIfSizeIsEqualMinSize():
    constructor = Sorted(5)
    s = constructor(None, 5)
    assert isinstance(s, _Sorted)


def test_Sorted_factory_shouldReturnDefaultIfSizeIsBelowMinSize():
    constructor = Sorted(5)
    s = constructor(someFolder, 1)
    assert isinstance(s, Default)


def test_Sorted_constructor():
    _Sorted(someFolder, length)


def test_Sorted_addOneItem():
    s = _Sorted(someFolder, length)
    s.add("item1")
    items = s.asList()
    assert len(items) is 1
    assert items[0] is "item1"


def test_Sorted_addTwoItems():
    s = _Sorted(someFolder, length)
    s.add("first item")
    s.add("second item")
    items = s.asList()
    assert len(items) is 2
    assert items[0] is "first item"
    assert items[1] is "second item"


def test_Sorted_shouldUseNaturalOrder():
    s = _Sorted(someFolder, length)
    s.add("z")
    s.add("a")
    items = s.asList()
    assert len(items) is 2
    assert items[0] is "a"
    assert items[1] is "z"


def test_Grouped_factory_defaultArguments():
    constructor = Grouped()
    s = constructor(None, 0)
    assert isinstance(s, _Grouped)


def test_Grouped_factory_shouldReturnSortedIfSizeIsAboveMinSize():
    constructor = Grouped(5)
    s = constructor(someFolder, 10)
    assert isinstance(s, _Grouped)


def test_Grouped_factory_shouldReturnSortedIfSizeIsEqualMinSize():
    constructor = Grouped(5)
    s = constructor(None, 5)
    assert isinstance(s, _Grouped)


def test_Grouped_factory_shouldReturnDefaultIfSizeIsBelowMinSize():
    constructor = Grouped(5)
    s = constructor(someFolder, 1)
    assert isinstance(s, Default)


def test_Grouped_constructor():
    _Grouped(someFolder, length)


def test_Grouped_add():
    g = _Grouped(someFolder, length)
    itemA1 = menu.Folder("A1 item")
    itemA2 = menu.Folder("a2 item")
    itemB1 = menu.Folder("b1 item")
    g.add(itemA1)
    g.add(itemA2)
    g.add(itemB1)
    items = g.asList()
    assert len(items) is 2
    aFolder = items[0]
    bFolder = items[1]
    assert aFolder.name() == "A (2)"
    assert len(aFolder.items()) is 2
    assert aFolder.items()[0] is itemA1
    assert aFolder.items()[1] is itemA2
    assert bFolder.name() == "B (1)"
    assert len(bFolder.items()) is 1
    assert bFolder.items()[0] is itemB1


def test_Grouped_asList_shouldReturnFlatListIfOnlyOneGroup():
    g = _Grouped(someFolder, length)
    itemA1 = menu.Folder("A1 item")
    itemA2 = menu.Folder("a2 item")
    g.add(itemA1)
    g.add(itemA2)
    items = g.asList()
    assert len(items) is 2
    assert items[0] is itemA1
    assert items[1] is itemA2
