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
    # # 定义Timer
    # Timer = None
    # # 将自己定义的timer封装成字典
    # timers = {}
    # # 封装的customnpc接口
    # c = None

    def __init__(self, _char):
        self.char = _char
        self.char.npc.say("Initialized!")
        self.Timer = MyTimer(_char.npc.getTimers())

        # define timerId
        self.timerAlarm = 1
        self.timerDuration = 2
        self.timerInterval = 3
        self.timerHang = 4

        self.Timer.add(self.timerAlarm, 40, False)
        self.Timer.add(self.timerDuration, 60, False)
        self.Timer.add(self.timerInterval, 140, False)
        self.Timer.add(self.timerHang, 100, False)

    def interact(self):
        pass

    def timer(self, timer_id):
        self.skill_rage(timer_id)

    def target(self):
        # self.timer_start("Alarm")
        self.Timer.start(self.timerAlarm)
        self.char.npc.say("警告:即将发动技能“癫狂连击”")

        # do something

    def targetLost(self):
        # self.timer_start("TimeToHang")
        self.Timer.start(self.timerHang)
        # do something

    # def timer_init(self):
    #     # 获取接口的Timer
    #     self.Timer = self.char.npc.getTimers()
    #     # 封装为字典，第一个参数为timerId，第二个为持续时间，第三个为是否循环; 外层表示是否正在进行
    #     self.timers["Alarm"] = [[1, 40, False], False]
    #     self.timers["Duration"] = [[2, 60, False], False]
    #     self.timers["Interval"] = [[3, 140, False], False]
    #     self.timers["TimeToHang"] = [[4, 100, False], False]

    def strengthen(self):
        self.char.npc.stats.melee.setStrength(6)
        self.char.npc.stats.melee.setDelay(4)

    def recover(self):
        self.char.npc.stats.melee.setStrength(7)
        self.char.npc.stats.melee.setDelay(16)

    def skill_rage(self, timer_id):
        # Alarm ends
        self.Timer.finish(timer_id)
        if timer_id == self.timerAlarm:
            self.char.npc.say("发动技能“癫狂连击”")
            # self.timer_start("Duration")
            self.Timer.start(self.timerDuration)
            # Strengthen
            self.strengthen()

        # Interval ends
        if timer_id == self.timerInterval:
            # 偷懒直接调用target(),反正效果一样（逃
            if self.char.npc.isAttacking():
                self.target()

        # Duration ends
        if timer_id == self.timerDuration:
            self.char.npc.say("“癫狂连击”结束")
            if self.char.npc.isAttacking():
                self.Timer.start(self.timerInterval)
            self.recover()

        # Hang ends
        if timer_id == self.timerHang:
            if not self.char.npc.isAttacking:
                self.recover()
                self.Timer.clear()

    # 调试函数
    # def show(self):
    #     print(dir(self.c.npc))
    #
    # def timer_test(self):
    #     self.c.npc.say('timer test')
    #     self.Timer.start(*self.timers['timer1'])


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
