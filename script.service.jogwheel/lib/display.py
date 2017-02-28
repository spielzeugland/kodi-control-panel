import RPi.GPIO as GPIO
from RPLCD import CharLCD
from simpleDisplay import Size20x4


class Display(Size20x4):

    def __init__(self, controller):
        super(Display, self).__init__(controller)
        self._configure()

    def _configure(self):
        # TODO make configurable
        GPIO.setmode(GPIO.BOARD)
        self._lcd = CharLCD(pin_backlight=40, backlight_mode=LCD.BacklightMode.active_high)

    def _write(self, lines):
        string = ""
        for line in lines:
            string = string + line
        self._lcd.write_string(string)

    def clear(self):
        self._lcd.clear()
