import context
import mocks
import time
import menu
from src.kodiMenu import AddonFolder, UrlFolder, UrlFile, FavouritesFolder, ShutdownAction, RebootAction


def test_UrlFolder_name_shouldReturnName():
    folder = UrlFolder(mocks.kodi.Kodi(), "newName", "url")
    assert folder.name() is "newName"


def test_UrlFile_name_shouldReturnName():
    folder = UrlFile(mocks.kodi.Kodi(), "newName", "url")
    assert folder.name() is "newName"


def test_FavouriteFolder_name_shouldReturnName():
    folder = FavouritesFolder(mocks.kodi.Kodi(), "newName")
    assert folder.name() is "newName"


def test_AddonFolder_name_shouldReturnName():
    folder = AddonFolder(mocks.kodi.Kodi(), "newName")
    assert folder.name() is "newName"


def test_FavouritesFolder_shouldBeAsync():
    kodi = mocks.kodi.Kodi()
    folder = FavouritesFolder(kodi)
    assert folder.async is True


def test_AddonFolder_shouldBeAsync():
    kodi = mocks.kodi.Kodi()
    folder = AddonFolder(kodi)
    assert folder.async is True


def test_UrlFolder_isDynamic_shouldBeAsync():
    kodi = mocks.kodi.Kodi()
    folder = UrlFolder(kodi, "name", "url")
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


def test_ShutdownAction_shouldBeSubClassOfAction():
    assert isinstance(ShutdownAction(None), menu.Action)


def test_ShutdownAction_init_shouldTakeName():
    action = ShutdownAction(None, "myName")
    assert action.name() == "myName"


def test_ShutdownAction_init_shouldUseDefaultName():
    assert ShutdownAction(None).name() == "Shutdown"


def test_ShutdownAction_run_shouldDelegateToKodi():
    kodi = mocks.kodi.Kodi()
    ShutdownAction(kodi).run(None)
    assert kodi.shutdownCnt == 1


def test_RebootAction_shouldBeSubClassOfAction():
    assert isinstance(RebootAction(None), menu.Action)


def test_RebootAction_init_shouldTakeName():
    action = RebootAction(None, "myName")
    assert action.name() == "myName"


def test_RebootAction_init_shouldUseDefaultName():
    assert RebootAction(None).name() == "Reboot"


def test_RebootAction_run_shouldDelegateToKodi():
    kodi = mocks.kodi.Kodi()
    RebootAction(kodi).run(None)
    assert kodi.rebootCnt == 1
