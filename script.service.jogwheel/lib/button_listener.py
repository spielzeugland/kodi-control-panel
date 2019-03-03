import RPi.GPIO as GPIO
import time
import threading


class ShutdownListener(threading.Thread):

    def __init__(self, pin, listener):
        threading.Thread.__init__(self)
        self.daemon = True
        self._running = True
        self._lock = threading.Lock()
        self._pin = pin
        self._listener = listener
        GPIO.setup(self._pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self._count = 0
        self._delay = 0.2
        queriesPerSecond = 1 / self._delay
        self._clickDelay = queriesPerSecond * 0.5  # up to 0.5s is click
        self._longClickDelay = queriesPerSecond * 2  # up to 2s is longClick
        self._veryLongClickDelay = queriesPerSecond * 5  # from 5s is veryLongClick

    def run(self):
        # TODO proper synchronization of _running
        while self._running:
            GPIO.wait_for_edge(self._pin, GPIO.BOTH)

            while self._running:
                current = not GPIO.input(self._pin)
                # print("read %s" % current)
                specificWait = 0
                if current:
                    self._count += 1
                    if self._count > self._veryLongClickDelay:
                        self._veryLongClick()
                        # TODO break here and let owner decide
                        return
                else:
                    if 0 < self._count <= self._clickDelay:
                        self._click()
                        specificWait = 1
                    elif self._clickDelay < self._count <= self._longClickDelay:
                        self._longClick()
                        specificWait = 2  # TODO why do we wait longer here?
                    self._count = 0
                    break
                if specificWait > 0:
                    time.sleep(specificWait)
                else:
                    time.sleep(self._delay)

    def _click(self):
        self._listener("click")

    def _longClick(self):
        self._listener("longClick")

    def _veryLongClick(self):
        self._listener("veryLongClick")

    def stop(self):
        with self._lock:
            self._running = False
