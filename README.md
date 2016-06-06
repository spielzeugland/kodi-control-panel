Easy hardware interface for Kodi
================================

Goal of this project is to offer a plugin for managing an easy hardware interface for Kodi e.g. for controlling Kodi on a RaspberryPi without need to have a monitor turned on.

It is currently under development and has not reached a usable state yet.

Development
-----------

Install requirements:

```
pip install -U pytest sniffer pycodestyle
```

Run the tests:
```
py.test test
```

Start sniffer (will run tests on save)
```
sniffer
```

What is missing?
-----------
- Locking (multithreading)
- Error handling
- Displaying messages
- Going back to Python 2.7 since Kodi does not offer Python 3
- Kodi Plugin wrapper
- ...
