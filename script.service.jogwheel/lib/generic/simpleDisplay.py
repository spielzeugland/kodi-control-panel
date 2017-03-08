import string
import traceback
import messages
from controller import Mode


class Size20x4(object):

    def __init__(self):
        self._columns = 20
        self._rows = 4
        self._debug = False
        self._emptyLine = self._columns * " "
        self._currentFolder = None
        self._currentItem = None
        self._currentMode = None

    def update(self, controller):
        lastMode = self._currentMode
        self._currentMode = controller.mode()
        lastItem = self._currentItem
        self._currentItem = controller.menu.item()
        lastFolder = self._currentFolder
        self._currentFolder = controller.menu.folder()

        modeChanged = lastMode is not self._currentMode
        itemChanged = lastItem is not self._currentItem
        folderChanged = lastFolder is not self._currentFolder

        if modeChanged:
            if self._currentMode is Mode.Player:
                self.writePlayer(controller)
            else:
                self.writeMenu(controller)
        elif itemChanged or folderChanged:
            self.writeMenu(controller)

        if self._debug:
            _printMessages()

    def writePlayer(self, controller):
        lines = _asLines(">>Player", self._columns, self._rows)
        self._write(lines)

    def writeMenu(self, controller):
        menu = controller.menu
        item = menu.item()
        folder = menu.folder()

        currentIndex = min(menu._currentIndex, 999)
        itemCnt = min(len(menu._currentItems), 999)

        sizeInfo = "[{0}/{1}]".format(currentIndex, itemCnt)
        titleLength = self._columns - len(sizeInfo) - 1

        isMainMenu = len(menu._menuStack) == 1

        if menu.isRoot():
            folderName = "Menu"
        else:
            folderName = menu.mainFolder().name()[0:titleLength]

        spaces = (titleLength - len(folderName)) * " "

        line1 = "{0}{1} {2}".format(folderName, spaces, sizeInfo)
        line2to4 = _asLines(_center(item.name(), self._columns - 2), self._columns, 3)
        lines = [line1] + line2to4
        self._write(lines)

    def writeMessage(self, message):
        lines = _asLines(message, self._columns, self._rows)
        self._write(lines)

    def clear(self):
        pass

    def close(self):
        pass

    def _write(self, lines):
        if self._debug:
            print("+" + (self._columns * "-") + "+")
        for line in lines:
            if self._debug:
                print("|" + line + "|")
            else:
                print(line)
        if self._debug:
            print("+" + (self._columns * "-") + "+")


def _asLines(text, columns, rows, border=1):
        maxLength = (columns * rows) - (rows * 2 * border)
        if maxLength < 1:
            return [" " * columns] * rows
        if len(text) > maxLength:
            if maxLength > len("..."):
                textEnd = maxLength - len("...")
                text = text[0:textEnd] + "..."
            else:
                text = text[0:maxLength]
        lines = []
        visibleColumns = columns - (2 * border)
        lineCnt = int(round(float(len(text)) / float(visibleColumns)))
        lineCnt = max(lineCnt, 1)
        hasLeadingLine = False
        borderSpaces = border * " "
        if lineCnt + 1 < rows:
            hasLeadingLine = True
            lines.append(columns * " ")
        for i in range(lineCnt):
            begin = i * visibleColumns
            end = begin + visibleColumns
            lineText = text[begin:end]
            spaces = (visibleColumns) - len(lineText)
            if spaces < 0:
                spaces = 0
            lines.append(borderSpaces + text[begin:end] + spaces * " " + borderSpaces)
        trailingLinesCnt = rows - lineCnt
        if hasLeadingLine:
            trailingLinesCnt = trailingLinesCnt - 1
        if trailingLinesCnt > 0:
            for i in range(trailingLinesCnt):
                lines.append(columns * " ")
        return lines


def _center(text, length):
        spaces = length - len(text)
        if spaces > 0:
            left = spaces // 2
            right = spaces % 2 + left
            return (left * " ") + text + (right * " ")
        else:
            return text


def _printMessages():
    if messages.hasUnread():
        unreadMessages = messages.getUnread()
        if len(unreadMessages) > 0:
            print("Messages:")
            for message in unreadMessages:
                print(message.text)
                if message.sysInfo is not None:
                    traceback.print_exception(message.sysInfo[0], message.sysInfo[1], message.sysInfo[2])
