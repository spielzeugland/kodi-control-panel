import context
import mocks
import time
import menu
from kodiMenu import *


def test_UrlFolder_name_shouldReturnName():
    folder = UrlFolder(mocks.kodi.Kodi(), "newName", "url")
    assert folder.name() is "newName"


def test_UrlFile_name_shouldReturnName():
    folder = UrlFile(mocks.kodi.Kodi(), "newName", "url")
    assert folder.name() is "newName"


def test_UrlFolder_isDynamic_shouldBeAsync():
    kodi = mocks.kodi.Kodi()
    folder = UrlFolder(kodi, "name", "url")
    assert folder.async is True


def test_UrlFolder_items_shouldReturnNoItems():
    kodi = mocks.kodi.Kodi()
    folder = UrlFolder(kodi, "folder", "something://folderUrl/")
    assert len(folder._loadItems()) == 0


def test_UrlFolder_items_shouldReturnOneFolder():
    url = "something://folderUrl/"
    kodi = mocks.kodi.Kodi()
    mocks.kodi.addFolder(kodi, url, "child1", "childUrl")
    folder = UrlFolder(kodi, "folder", url)
    items = folder._loadItems()
    assert len(items) == 1
    assert items[0].__class__ is UrlFolder
    assert items[0].name() == "child1"
    assert items[0]._url == "childUrl"


def test_UrlFolder_items_shouldReturnOneFile():
    url = "something://folderUrl/"
    kodi = mocks.kodi.Kodi()
    mocks.kodi.addFile(kodi, url, "child1", "childUrl")
    folder = UrlFolder(kodi, "folder", url)
    items = folder._loadItems()
    assert len(items) == 1
    assert items[0].__class__ is UrlFile
    assert items[0].name() == "child1"
    assert items[0]._url == "childUrl"


def test_UrlFolder_items_shouldReturnOneFolderAndOneFile():
    url = "something://folderUrl/"
    kodi = mocks.kodi.Kodi()
    mocks.kodi.addFolder(kodi, url, "child1", "childUrl")
    mocks.kodi.addFile(kodi, url, "child1", "childUrl")
    folder = UrlFolder(kodi, "folder", url)
    items = folder._loadItems()
    assert len(items) == 2
    assert items[0].__class__ is UrlFolder
    assert items[1].__class__ is UrlFile


def test_UrlFile_run_shouldCallPlayOnKodi():
    kodi = mocks.kodi.Kodi()
    file = UrlFile(kodi, "myFileName", "myFileUrl")
    file.run(None)
    time.sleep(0.1)
    assert kodi.playWasCalledWith("myFileUrl") is True


def test_UrlFile_run_shouldNotCallPlayOnKodiIfCurrentlyBusy():
    kodi = mocks.kodi.Kodi()
    mocks.kodi.addPlayDelay(kodi, 0.1)
    file = UrlFile(kodi, "myFileName", "myFileUrl")
    file.run(None)
    file.run(None)
    time.sleep(0.3)
    assert kodi._playCnt == 1
