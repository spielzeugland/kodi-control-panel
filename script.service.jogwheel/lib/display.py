import RPi.GPIO as GPIO
from RPLCD import CharLCD


class Display(object):

    def __init__(self, controller):
        self._configure()
        self._controller = controller

    def _configure(self):
        # TODO make configurable
        GPIO.setmode(GPIO.BOARD)
        self._lcd = CharLCD(pin_rw=5)

    def update(self):
        # TODO implement
        pass

    def write(self, string):
        self._lcd.write_string(string)

    def clear(self):
        self._lcd.clear()

    def close(self):
        pass
