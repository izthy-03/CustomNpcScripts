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

def died(c):
    global test
    test.died()

class Entity:
    def __init__(self, _char):
        self.char = _char
        self.char.npc.say("Initialized!")
        self.Timer = MyTimer(_char.npc.getTimers())

        # define timerId
        self.timerInterval = 3
        self.timerAlarm = 1
        self.timerCheck = 4

        self.Timer.add(self.timerAlarm, 100, False)
        self.Timer.add(self.timerInterval, 200, False)
        self.Timer.add(self.timerCheck, 107, True)

        self.Timer.stop(self.timerCheck)
        self.Timer.start(self.timerCheck)

        self.skillRange = 5

        # print(dir(self.char.npc))

    def interact(self):
        pass

    def timer(self, timer_id):
        self.Timer.finish(timer_id)

        if timer_id == self.timerCheck:
            # self.char.npc.say("check " + str(self.char.npc.isAttacking()))

            if not self.char.npc.isAttacking():
                # self.char.npc.say("clear")
                self.Timer.clear()
                self.Timer.start(self.timerCheck)
                self.reset()
        else:
            self.skill(timer_id)

    def target(self):
        self.Timer.start(self.timerInterval)

    def targetLost(self):
        pass

    def skill(self, timer_id):
        if timer_id == self.timerAlarm:
            self.reset()
            self.Timer.start(self.timerInterval)

        if timer_id == self.timerInterval:
            self.prepare()

    def prepare(self):
        # self.char.npc.playAnimation(0)
        self.char.npc.addPotionEffect(81, 1, 0, False)
        self.char.npc.addPotionEffect(2, 9999, 255, False)
        self.circleExplode(self.skillRange, "cloud")
        for entity in self.char.npc.world.getNearbyEntities(self.char.npc.pos, 5, 1000):
            if entity != self.char.npc:
                x = entity.x - self.char.npc.x
                z = entity.z - self.char.npc.z
                cita = math.degrees(math.atan2(x,z))
                cita = self.char.npc.rotation + cita
                entity.knockback(4, cita)
        self.char.npc.addPotionEffect(10, 100, 5, False)
        self.Timer.start(self.timerAlarm)

    def damaged(self):
        if self.char.npc.isAttacking() and self.Timer.isRunning[self.timerAlarm]:
            self.Timer.stop(self.timerAlarm)
            self.Timer.start(self.timerInterval)
            self.reset()

    def reset(self):
        self.char.npc.clearPotionEffects()

    def circle(self, radius, particle):
        thisX = self.char.npc.getX()
        thisY = self.char.npc.getY()
        thisZ = self.char.npc.getZ()
        for i in range(0, 360, 5):
            rad = i * math.pi / 180
            px = radius * math.cos(rad) + thisX
            pz = radius * math.sin(rad) + thisZ
            py = thisY
            self.char.npc.world.spawnParticle(particle, px, py, pz, 0, 0, 0, 0, 5)

    def circleExplode(self, radius, particle):
        thisX = self.char.npc.getX()
        thisY = self.char.npc.getY()
        thisZ = self.char.npc.getZ()
        for i in range(0, 360, 5):
            rad = i * math.pi / 180
            dx = math.cos(rad)
            dz = math.sin(rad)
            self.char.npc.world.spawnParticle(
                particle, thisX, thisY + 1, thisZ, dx, 0, dz, 0.5, 5
            )
    
    def died(self):
        self.char.npc.executeCommand("/title @a title {\"text\":\"Enemy felled\",\"color\":\"yellow\"}")


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