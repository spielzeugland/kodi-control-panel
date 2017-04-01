Easy hardware interface for Kodi
================================

.. image:: https://travis-ci.org/spielzeugland/kodi-control-panel.svg
    :target: https://travis-ci.org/spielzeugland/kodi-control-panel
.. image:: https://coveralls.io/repos/spielzeugland/kodi-control-panel/badge.svg
    :target: https://coveralls.io/r/spielzeugland/kodi-control-panel

Goal of this project is to offer a plugin for managing an easy hardware interface for Kodi e.g. for controlling Kodi on a RaspberryPi without need to have a monitor turned on.

It is currently under development and has not reached a usable state yet.

Development
-----------

Install requirements:

.. code-block::

     pip install -r requirements-dev.txt


Run the tests:

.. code-block::

    python tests.py


Start sniffer (will run tests on save)

.. code-block::

     sniffer


Run coverage

.. code-block::

    coverage run tests.py


View coverage report run ``coverage html`` and open `index.html` from `coverage` folder or just run ``coverage report``.


What is missing?
-----------
- Configuration of PINs etc.
- Error handling
- Logging
- Displaying messages
- Kodi Plugin wrapper
- Multilanguage support
- ...
