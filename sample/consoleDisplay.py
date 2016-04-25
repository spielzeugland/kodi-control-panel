import time
from threading import Thread

class ConsoleDisplay:
	def __init__(self, menu):
		self._menu = menu
		self._prevFolder = None
		self._prevItem = None
		self._shouldStop = False
	def _run(self):
		while not self._shouldStop:
			time.sleep(1)
			folder = self._menu.folder()
			item = self._menu.item()
			if(folder is not self._prevFolder or item is not self._prevItem):
				print("%s > %s [%s/%s]" % (folder.name(), item.name(), self._menu._currentIndex, len(self._menu._currentItems)))
				self._prevFolder = folder
				self._prevItem = item
	def open(self):
		Thread(target=self._run).start()
		cmd = ""
		while cmd != "exit":
			cmd = input();
			if cmd == "x":
				self._menu.moveBy(1)
			elif cmd == "xx":
				self._menu.moveBy(2)
			elif cmd == "y":
				self._menu.moveBy(-1)
			elif cmd == "yy":
				self._menu.moveBy(-2)
			elif cmd == "s":
				self._menu.select()
			elif cmd == "b":
				self._menu.back()
			elif cmd == "r":
				self._menu.reset()
			elif cmd == "exit":
				self.close()
	def close(self):
		self._shouldStop = True
