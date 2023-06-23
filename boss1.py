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
    # 定义Timer
    Timer = None
    # 将自己定义的timer封装成字典
    timers = {}
    # 封装的customnpc接口
    c = None

    def __init__(self, c):
        self.c = c
        self.c.npc.say("Initialized!")
        self.timer_init()

    def interact(self):
        pass

    def timer(self, timer_id):
        self.skill_rage(timer_id)

    def target(self):
        self.timer_start("Alarm")
        self.c.npc.say("警告:即将发动技能“癫狂连击”")

        # do something

    def targetLost(self):
        self.timer_start("TimeToHang")
        # do something

    def timer_init(self):
        # 获取接口的Timer
        self.Timer = self.c.npc.getTimers()
        # 封装为字典，第一个参数为timerId，第二个为持续时间，第三个为是否循环; 外层表示是否正在进行
        self.timers["Alarm"] = [[1, 40, False], False]
        self.timers["Duration"] = [[2, 60, False], False]
        self.timers["Interval"] = [[3, 140, False], False]
        self.timers["TimeToHang"] = [[4, 100, False], False]

    def timer_start(self, timer_name):
        if not self.timers[timer_name][1]:
            self.timers[timer_name][1] = True
            self.Timer.start(*self.timers[timer_name][0])

    def timer_finish(self, timer_name):
        self.timers[timer_name][1] = False

    def strengthen(self):
        self.c.npc.stats.melee.setStrength(6)
        self.c.npc.stats.melee.setDelay(4)

    def recover(self):
        self.c.npc.stats.melee.setStrength(7)
        self.c.npc.stats.melee.setDelay(16)

    def skill_rage(self, timer_id):
        # Alarm ends
        if timer_id == self.timers["Alarm"][0][0]:
            self.timer_finish("Alarm")
            self.c.npc.say("发动技能“癫狂连击”")
            self.timer_start("Duration")
            # Strengthen
            self.strengthen()

        # Interval ends
        if timer_id == self.timers["Interval"][0][0]:
            self.timer_finish("Interval")
            # 偷懒直接调用target(),反正效果一样（逃
            if self.c.npc.isAttacking():
                self.target()

        # Duration ends
        if timer_id == self.timers["Duration"][0][0]:
            self.timer_finish("Duration")
            self.c.npc.say("“癫狂连击”结束")
            if self.c.npc.isAttacking():
                self.timer_start("Interval")
            self.recover()

        # Hang ends
        if timer_id == self.timers["TimeToHang"][0][0]:
            self.timer_finish("TimeToHang")
            if not self.c.npc.isAttacking:
                self.recover()
                self.Timer.clear()

    # 调试函数
    # def show(self):
    #     print(dir(self.c.npc))
    #
    # def timer_test(self):
    #     self.c.npc.say('timer test')
    #     self.Timer.start(*self.timers['timer1'])
