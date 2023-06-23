# 定义测试npc
test = None


# hook必须暴露在外，曲折实现封装
def init(c):
    global test
    # 实例化
    test = Entity(c)


def interact(c):
    global test
    test.interact()


def timer(c):
    global test
    # print(dir(c))
    # 将触发timerEvent的timerId传给test
    test.timer(c.id)


def target(c):
    global test
    test.target()


def targetLost(c):
    global test
    test.targetLost()


class Entity:
    def __init__(self, _char):
        self.char = _char
        self.char.npc.say("Initialized!")
        self.Timer = MyTimer(_char.npc.getTimers())

        # define timerId
        self.timerInterval = 3
        self.timerAlarm = 1

        self.Timer.add(self.timerAlarm, 20, False)
        self.Timer.add(self.timerInterval, 100, False)

    def interact(self):
        pass

    def timer(self, timer_id):
        self.skill(timer_id)

    def target(self):
        # self.timer_start("Alarm")
        self.Timer.start(self.timerInterval)
        # self.char.npc.say("警告:即将发动技能“癫狂连击”")

        # do something

    def targetLost(self):
        # self.timer_start("TimeToHang")
        self.Timer.start(self.timerHang)
        self.Timer.clear()
        # do something

    def skill(self, timer_id):
        self.Timer.finish(timer_id)

        if timer_id == self.timerAlarm:
            self.quake()
            self.Timer.start(self.timerInterval)

        if timer_id == self.timerInterval:
            self.Timer.start(self.timerAlarm)

    def quake(self):
        pass


class MyTimer:
    def __init__(self, timer):
        self.Timer = timer
        self.timers = []
        self.isRunning = []

    # Add a timer
    def add(self, timerId, ticks, repeat=False):
        while timerId >= len(self.timers):
            self.timers.append([0, 0, 0])
            self.isRunning.append(False)
        self.timers[timerId] = [timerId, ticks, repeat]

    def start(self, timerId):
        if not self.isRunning[timerId]:
            self.isRunning[timerId] = True
            self.Timer.start(*self.timers[timerId])

    def finish(self, timerId):
        self.isRunning[timerId] = False

    def stop(self, timerId):
        self.Timer.stop(timerId)
        self.isRunning[timerId] = False

    def clear(self):
        self.Timer.clear()
        for i in range(0, len(self.isRunning)):
            self.isRunning[i] = False
