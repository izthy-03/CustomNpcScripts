import math

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


def damaged(c):
    global test
    test.damaged()


class Entity:
    def __init__(self, _char):
        self.char = _char
        self.char.npc.say("Initialized!")
        self.Timer = MyTimer(_char.npc.getTimers())

        # define timerId
        self.timerAlarm = 1
        self.timerInterval = 3
        self.timerHang = 4

        self.Timer.add(self.timerAlarm, 15, False)
        self.Timer.add(self.timerInterval, 40, False)
        self.Timer.add(self.timerHang, 100, False)

        # 验证这场战斗中是否已经发生过狂暴；验证是否有目标，只有有目标时才能狂暴
        self.CheckBerserk = False
        self.Targeted = False

    def interact(self):
        pass

    def damaged(self):
        health = self.char.npc.getHealth()
        if health <= 80 and self.Targeted and self.CheckBerserk:
            self.CheckBerserk = True
            self.Timer.start(self.timerInterval)
            # 狂暴
            self.char.npc.stats.ranged.setStrength(12)
            self.char.npc.stats.ranged.setDelay(20, 60)
            self.char.npc.stats.ranged.setSpeed(14)
            self.char.npc.stats.setCombatRegen(0)
            self.circleExplode(1, "lava")

    def timer(self, timer_id):
        self.skill(timer_id)

    def target(self):
        self.Targeted = True

    def targetLost(self):
        self.Timer.start(self.timerHang)

    def recover(self):
        self.char.npc.stats.ranged.setStrength(10)
        self.char.npc.stats.ranged.setDelay(40, 80)
        self.char.npc.stats.ranged.setSpeed(11)
        self.char.npc.stats.setCombatRegen(1)
        self.CheckBerserk = False
        self.Targeted = False

    def skill(self, timer_id):
        # Alarm ends
        self.Timer.finish(timer_id)
        if timer_id == self.timerAlarm:
            self.Timer.start(self.timerInterval)
            self.char.npc.say("Skill!")
            # 释放技能

        # Interval ends
        if timer_id == self.timerInterval:
            self.Timer.start(self.timerAlarm)
            self.char.npc.say("Alarm!")
            self.Explode(1, "cloud")
            # 开始预警

        # Hang ends
        if timer_id == self.timerHang:
            if not self.char.npc.isAttacking():
                self.recover()
                self.Timer.clear()

    def circleExplode(self, radius, particle):
        thisX = self.char.npc.getX()
        thisY = self.char.npc.getY()
        thisZ = self.char.npc.getZ()
        for i in range(0, 360, 5):
            rad = i * math.pi / 180
            dx = math.cos(rad)
            dz = math.sin(rad)
            self.char.npc.world.spawnParticle(
                particle, thisX, thisY + 1, thisZ, dx, 0, dz, 0.01, 5
            )

    def cannon(self, radius, particle):
        for i in range(0, 360, 5):
            rad = i * math.pi / 180
            dx = math.cos(rad)
            dz = math.sin(rad)
            self.char.npc.world.spawnParticle(
                particle, 1895, 101, 116, dx, 0, dz, 0.01, 5
            )
            self.char.npc.world.spawnParticle(
                particle, 1895, 101, 130, dx, 0, dz, 0.01, 5
            )


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
