import RPi.GPIO as GPIO

from display import Display
from rotary_encoder import RotaryEncoder
from button_listener import ButtonListener


def _asEvent(name, data=None):
    return {"name": name, "data": data}


class Hardware(object):

    def __init__(self, queue):
        self._display = Display
        self._inputs = _Inputs(queue, self._display)

    def update(self, event):
        self._display.update(event)

    def close(self):
        self._inputs.close()


class _Inputs(object):

    def __init__(self, queue, display):
        self._button = None
        self._rotary = None
        self._display = display
        self._configure(queue)

    def _configure(self, queue):
        # TODO make configurable
        buttonPin = 5
        channelA = 11
        channelB = 13

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        rotaryListener = lambda(delta): queue.put_nowait(_asEvent("moveBy", delta))
        self._rotary = RotaryEncoder.Worker(channelA, channelB, rotaryListener)
        self._rotary.start()
        
        buttonListener = lambda(action): queue.put_nowait(_asEvent(action, self._display._currentItem))
        self._button = ButtonListener(buttonPin, buttonListener)
        self._button.start()

    def close(self):
        # TODO error handling
        self._button.stop()
        self._rotary.stop()
