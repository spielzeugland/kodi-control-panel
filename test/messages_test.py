import context
import mocks
import messages


def test_hasShouldReturnFalseAfterClear():
    messages._clear()
    assert messages.hasUnread() is False


def test_addShouldStoreMessage():
    messages.add("my message")
    assert messages.hasUnread() is True


def test_callingAddTwiceshouldStoreTwoMessages():
    messages.add("my message1")
    messages.add("my message2")
    assert messages.hasUnread() is True


def test_getUnreadShouldRetrieveUnreadMessage():
    messages._clear()
    messages.add("my new message")
    unread = messages.getUnread()
    assert len(unread) is 1
    assert unread[0].text == "my new message"


def test_getUnreadShouldRetrieveMultipleUnreadMessagesSortedByLatestFirst():
    messages._clear()
    messages.add("my 1st message")
    messages.add("my 2nd message")
    unread = messages.getUnread()
    assert len(unread) is 2
    assert unread[0].text == "my 2nd message"
    assert unread[1].text == "my 1st message"


def test_getUnreadShouldClearUnreadMessages():
    messages._clear()
    messages.add("my new message")
    unread = messages.getUnread()
    assert messages.hasUnread() is False


def test_archiveShouldContainUnreadMessages():
    messages._clear()
    messages.add("my unread message")
    archived = messages.archive()
    assert len(archived) is 1
    assert archived[0].text == "my unread message"


def test_archiveShouldReturnAllMessagesSortedByLatestFirst():
    messages._clear()
    messages.add("my 1st message")
    messages.add("my 2nd message")
    unread = messages.getUnread()
    messages.add("my 3rd message")
    unread = messages.getUnread()
    archived = messages.archive()
    assert len(archived) is 3
    assert archived[0].text == "my 3rd message"
    assert archived[1].text == "my 2nd message"
    assert archived[2].text == "my 1st message"


def test_archiveSizeShouldNotBeExceeded():
    oldSize = messages._archiveSize
    messages._archiveSize = 10
    try:
        messages._clear()
        for index in range(20):
            messages.add("some message")
        assert len(messages.archive()) is 10
    finally:
        messages._archiveSize = oldSize


def test_callingHasMultipleTimes_shouldReturnSameValue():
    messages.add("my message")
    assert messages.hasUnread() is True
    assert messages.hasUnread() is True


def test_addShouldUseDefaultTextForMissingDetails():
    messages._clear()
    messages.add("my message")
    unread = messages.getUnread()
    assert len(unread) is 1
    assert unread[0].details == "No details provided"
