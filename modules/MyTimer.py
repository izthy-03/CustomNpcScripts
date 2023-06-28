class MyTimer:
    def __init__(self, timer) -> None:
        self.Timer = timer
        self.timers = []
        self.isRunning = []

    # Add a timer
    def add(self, timerId: int, ticks: int, repeat=False):
        self.timers[timerId] = [timerId, ticks, repeat]

    def start(self, timerId: int):
        if not self.isRunning[timerId]:
            self.isRunning[timerId] = True
            self.Timer.start(*self.timers[timerId])

    def finish(self, timerId: int):
        self.isRunning[timerId] = False

    def stop(self, timerId: int):
        self.Timer.stop(timerId)
        self.isRunning[timerId] = False

    def clear(self):
        self.Timer.clear()
        for i in range(0, len(self.isRunning)):
            self.isRunning[i] = False

    def modify(self, timerId, ticks, repeat):
        self.timers[timerId] = [timerId, ticks, repeat]