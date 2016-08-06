def start(kodi, controller, inputs, display):
    display.write("Welcome")
    _mainloop(kodi, controller, inputs, display)
    display.clear()
    display.write("Shuting down...")


def _mainloop(kodi, controller, inputs, display):
    monitor = kodi.getMonitor()
    while not inputs.shutdown() or monitor.abortRequested():

        # TODO using simple polling in a mainloop for now
        display.update()

        if monitor.waitForAbort(0.1):
            break
