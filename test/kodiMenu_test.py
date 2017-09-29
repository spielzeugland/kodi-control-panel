import context
import mocks
import time
import menu
from kodiMenu import *


def test_FavouriteFolder_name_shouldReturnName():
    folder = FavouritesFolder(mocks.kodi.Kodi(), "newName")
    assert folder.name() is "newName"


def test_AddonFolder_name_shouldReturnName():
    folder = AddonFolder(mocks.kodi.Kodi(), "newName")
    assert folder.name() is "newName"


def test_ChannelGroupFolder_name_shouldReturnName():
    folder = ChannelGroupFolder(mocks.kodi.Kodi(), "newName", "type")
    assert folder.name() is "newName"


def test_ChannelFolder_name_shouldReturnName():
    folder = ChannelFolder(mocks.kodi.Kodi(), "newName", 7)
    assert folder.name() is "newName"


def test_FavouritesFolder_shouldBeAsync():
    kodi = mocks.kodi.Kodi()
    folder = FavouritesFolder(kodi)
    assert folder.async is True


def test_ChannelGroupFolder_shouldBeAsync():
    kodi = mocks.kodi.Kodi()
    folder = ChannelGroupFolder(kodi, "name", "type")
    assert folder.async is True


def test_ChannelFolder_shouldBeAsync():
    kodi = mocks.kodi.Kodi()
    folder = ChannelFolder(kodi, "name", 7)
    assert folder.async is True


def test_AddonFolder_shouldBeAsync():
    kodi = mocks.kodi.Kodi()
    folder = AddonFolder(kodi)
    assert folder.async is True


def test_FavouritesFolder_items_shouldReturnNoItems():
    kodi = mocks.kodi.Kodi()
    folder = FavouritesFolder(kodi)
    assert len(folder._loadItems()) == 0


def test_FavouritesFolder_items_shouldReturnOneItem():
    kodi = mocks.kodi.Kodi()
    mocks.kodi.addFavourite(kodi, "a1", "id1")
    folder = FavouritesFolder(kodi)
    items = folder._loadItems()
    assert len(items) is 1
    assert items[0].name() == "a1"
    assert items[0]._url == "id1"


def test_FavouritesFolder_items_shouldReturnTwoItem():
    kodi = mocks.kodi.Kodi()
    mocks.kodi.addFavourite(kodi, "a1", "id1")
    mocks.kodi.addFavourite(kodi, "a2", "id2")
    folder = FavouritesFolder(kodi)
    items = folder._loadItems()
    assert len(items) is 2
    assert items[0].name() == "a1"
    assert items[0]._url == "id1"
    assert items[1].name() == "a2"
    assert items[1]._url == "id2"


def test_AddonFolder_items_shouldReturnOneItem():
    kodi = mocks.kodi.Kodi()
    mocks.kodi.addAddon(kodi, "a1", "id1")
    folder = AddonFolder(kodi)
    items = folder._loadItems()
    assert len(items) is 1
    assert items[0].name() == "a1"
    assert items[0]._url == "plugin://id1/"


def test_AddonFolder_items_shouldReturnTwoItems():
    kodi = mocks.kodi.Kodi()
    mocks.kodi.addAddon(kodi, "a1", "id1")
    mocks.kodi.addAddon(kodi, "a2", "id2")
    folder = AddonFolder(kodi)
    items = folder._loadItems()
    assert len(items) == 2
    assert items[0].name() == "a1"
    assert items[0]._url == "plugin://id1/"
    assert items[1].name() == "a2"
    assert items[1]._url == "plugin://id2/"


def test_AddonFolder_items_shouldReturnNoItems():
    kodi = mocks.kodi.Kodi()
    folder = AddonFolder(kodi)
    items = folder._loadItems()
    assert len(items) == 0
