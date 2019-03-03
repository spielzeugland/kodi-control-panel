import worker


def start(queue, controller):
    def _handle():
        event = queue.get()
        name = event["name"]
        moveCount = 0
        while name is "moveBy":
            moveCount = moveCount + event["data"]
            try:
                event = queue.get(True, 0.1)
                name = event["name"]
            except:
                name = None
        if moveCount is not 0:
            controller.moveBy(moveCount)
        if name is "click":
            controller.click(event["data"])
            return True
        elif name is "longClick":
            controller.longClick()
            return True
        elif name is "veryLongClick":
            # TODO find better way to signal shutdown which also works with Kodi Monitors
            return False
    return worker.runAsLoop(_handle)
