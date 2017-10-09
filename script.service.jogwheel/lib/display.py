from threading import Lock
import RPi.GPIO as GPIO
import RPLCD as LCD
from generic.simpleDisplay import Size20x4


class Display(Size20x4):

    def __init__(self):
        super(Display, self).__init__()
        self._configure()
        self._lock = Lock()

    def _configure(self):
        # TODO make configurable
        GPIO.setmode(GPIO.BOARD)
        self._lcd = LCD.CharLCD(pin_backlight=40, backlight_mode=LCD.BacklightMode.active_high)

    def _write(self, lines):
        string = ""
        # TODO what is the pythonic way for this?
        for line in lines:
            string = string + line
        with self._lock:
            self._lcd.write_string(string)

    def clear(self):
        with self._lock:
            self._lcd.clear()

    def backlight(self, on):
        with self._lock:
            self._lcd.backlight_enabled = on
