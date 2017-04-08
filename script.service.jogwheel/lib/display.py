import RPi.GPIO as GPIO
import RPLCD as LCD
from generic.simpleDisplay import Size20x4


class Display(Size20x4):

    def __init__(self):
        super(Display, self).__init__()
        self._configure()

    def _configure(self):
        # TODO make configurable
        GPIO.setmode(GPIO.BOARD)
        self._lcd = LCD.CharLCD(pin_backlight=40, backlight_mode=LCD.BacklightMode.active_high)

    def _write(self, lines):
        string = ""
        # TODO what is the pythonic way for this?
        for line in lines:
            string = string + line
        self._lcd.write_string(string)

    def clear(self):
        self._lcd.clear()
