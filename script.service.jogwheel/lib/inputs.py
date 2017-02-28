import RPi.GPIO as GPIO

from rotary_encoder import RotaryEncoder
from button_listener import ShutdownListener


class Inputs(object):

    def __init__(self, controller):
        self._button = None
        self._rotary = None
        self._controller = controller
        self._configure()

    def _configure(self):
        # TODO make configurable
        shutdownPin = 5
        channelA = 11
        channelB = 13

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(shutdownPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self._rotary = RotaryEncoder.CyclesWorker(channelA, channelB)
        self._rotary.start()
        self._button = ShutdownListener(shutdownPin)
        self._button.start()

    def close(self):
        # TODO  error handling
        self._button.stop()
        self._rotary.stop()
