import RPi.GPIO as GPIO
import time
import threading


class ShutdownListener(threading.Thread):

    def __init__(self, shutdownPin):
        threading.Thread.__init__(self)
        self.daemon = True
        self.lock = threading.Lock()
        self.shutdownPin = shutdownPin
        GPIO.setup(shutdownPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.count = 0
        self.shutdownState = False
        self.selectState = False
        self.backState = False
        self.delay = 0.2
        self.factor = 1 / self.delay
        self.select_delay = self.factor * 0.5
        self.back_delay = self.factor * 2
        self.shutdown_delay = self.factor * 5
        self._stopping = False

    def run(self):
        while not self._stopping:
            GPIO.wait_for_edge(self.shutdownPin, GPIO.BOTH)

            while not self._stopping:
                current = not GPIO.input(self.shutdownPin)
                # print("read %s" % current)
                with self.lock:
                    specificWait = 0
                    if current:
                        self.count += 1
                        if self.count > self.shutdown_delay:
                            self.shutdownState = True
                            return
                    else:
                        if(0 < self.count < self.select_delay):
                            self.selectState = True
                            specificWait = 1
                        elif (self.select_delay < self.count < self.back_delay):
                            self.backState = True
                            specificWait = 2
                        self.count = 0
                        break
                if(specificWait > 0):
                    time.sleep(specificWait)
                else:
                    time.sleep(self.delay)

    def shutdown(self):
        with self.lock:
            temp = self.shutdownState
            self.shutdownState = False
            return temp

    def selected(self):
        with self.lock:
            temp = self.selectState
            self.selectState = False
            return temp

    def back(self):
        with self.lock:
            temp = self.backState
            self.backState = False
            return temp

    def stop(self):
        self.stopping = True
