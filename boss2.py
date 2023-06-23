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


class Entity:
    def __init__(self, _char):
        self.char = _char
        self.char.npc.say("Initialized!")
        self.Timer = MyTimer(_char.npc.getTimers())

        # define timerId
        self.timerInterval = 3
        self.timerAlarm = 1
        self.timerHang = 4

        self.Timer.add(self.timerAlarm, 10, False)
        self.Timer.add(self.timerInterval, 100, False)
        self.Timer.add(self.timerHang, 100, False)

        self.skillRange = 9

        # print(dir(self.char.npc))

    def interact(self):
        pass

    def timer(self, timer_id):
        if timer_id == self.timerHang and not self.char.npc.isAttacking:
            self.Timer.clear()
            self.reset()
        else:
            self.skill(timer_id)

    def target(self):
        self.Timer.start(self.timerInterval)

    def targetLost(self):
        # 5秒待机，防止切换仇恨时技能重置
        self.Timer.start(self.timerHang)

    def skill(self, timer_id):
        self.Timer.finish(timer_id)

        if timer_id == self.timerAlarm:
            self.quake()
            self.Timer.start(self.timerInterval)

        if timer_id == self.timerInterval:
            self.prepare()
            self.Timer.start(self.timerAlarm)

    def prepare(self):
        # self.char.npc.playAnimation(0)
        self.char.npc.addPotionEffect(2, 9999, 255, False)
        self.circle(self.skillRange, "largesmoke")

    def quake(self):
        players = self.char.npc.world.getAllPlayers()
        thisY = self.char.npc.getY()
        thisPos = self.char.npc.getPos()
        # self.char.npc.say("my Y = " + str(thisY))
        self.circleExplode(self.skillRange, "flame")
        for player in players:
            coordY = player.getY()
            # name = player.getName()
            # self.char.npc.say(name + " y = " + str(coordY))
            distance = player.getPos().distanceTo(thisPos)
            if abs(coordY - thisY) <= 0.92 and distance <= self.skillRange:
                player.damage(15)

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
