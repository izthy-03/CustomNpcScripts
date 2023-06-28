import math
import random

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
        self.timerCheck = 4

        self.Timer.add(self.timerAlarm, 6, False)
        self.Timer.add(self.timerInterval, 100, False)
        self.Timer.add(self.timerCheck, 107, True)

        self.Timer.stop(self.timerCheck)
        self.Timer.start(self.timerCheck)


        # 矩形范围技能统一定义
        self.sX1 = self.char.npc.x
        self.sZ1 = self.char.npc.z
        self.sX2 = self.char.npc.x
        self.sZ2 = self.char.npc.z
        self.sX3 = self.char.npc.x
        self.sZ3 = self.char.npc.z
        self.sX4 = self.char.npc.x
        self.sZ4 = self.char.npc.z
        self.sY = self.char.npc.y
        self.cita = self.char.npc.rotation
        self.skillLenth = 6.0
        self.skillWidth = 1.0

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
        # 5秒待机，防止切换仇恨时技能重置
        # self.Timer.start(self.timerHang)
        pass

    def skill(self, timer_id):
        if timer_id == self.timerAlarm:
            self.smite()
            ranSmite = random.randint(40, 120)
            self.Timer.modify(self.timerInterval, ranSmite, False)
            self.Timer.start(self.timerInterval)

        if timer_id == self.timerInterval:
            self.prepare()
            self.Timer.start(self.timerAlarm)

    def prepare(self):
        # self.char.npc.playAnimation(0)
        self.char.npc.addPotionEffect(2, 9999, 255, False)
        self.cita = self.char.npc.rotation
        if abs(self.cita) >= 360:
            self.cita = self.cita % 360
        self.cita = self.cita * math.pi / 180
        for i in range(1, int(self.skillLenth) + 1):
            Lenth = float(i)
            pX = self.char.npc.x - math.sin(self.cita) * Lenth
            pZ = self.char.npc.z + math.cos(self.cita) * Lenth
            pY = self.char.npc.y + 0.5
            self.thisPartical(pX, pY, pZ, "cloud")
        self.sX1 = self.char.npc.x - math.cos(self.cita) * self.skillWidth
        self.sZ1 = self.char.npc.z - math.sin(self.cita) * self.skillWidth
        self.sX2 = self.char.npc.x + math.cos(self.cita) * self.skillWidth
        self.sZ2 = self.char.npc.z + math.sin(self.cita) * self.skillWidth
        self.sX3 = self.sX1 - math.sin(self.cita) * self.skillLenth
        self.sZ3 = self.sZ1 + math.cos(self.cita) * self.skillLenth
        self.sX4 = self.sX2 - math.sin(self.cita) * self.skillLenth
        self.sZ4 = self.sZ2 + math.cos(self.cita) * self.skillLenth
        self.sY = self.char.npc.y



    def smite(self):
        for entity in self.char.npc.world.getNearbyEntities(self.char.npc.pos, 9, 1000):
            if entity != self.char.npc:
                x = entity.x
                y = entity.y
                z = entity.z
                a1 = (self.sX2-self.sX1,self.sZ2-self.sZ1)
                b1 = (x-self.sX1,z-self.sZ1)
                t1 = a1[0]*b1[1]-a1[1]*b1[0]
                a2 = (self.sX4-self.sX3,self.sZ4-self.sZ3)
                b2 = (x-self.sX3,z-self.sZ3)
                t2 = a2[0]*b2[1]-a2[1]*b2[0]
                a3 = (self.sX3-self.sX2,self.sZ3-self.sZ2)
                b3 = (x-self.sX2,z-self.sZ2)
                t3 = a3[0]*b3[1]-a3[1]*b3[0]
                a4 = (self.sX1-self.sX4,self.sZ1-self.sZ4)
                b4 = (x-self.sX4,z-self.sZ4)
                t4 = a4[0]*b4[1]-a4[1]*b4[0]
                if t1 * t2 <= 0 and t3 * t4 >= 0 and (y - self.sY) <= 2:
                    entity.damage(16)
                    entity.addPotionEffect( 2, 3, 4, False)
            for i in range(1, int(self.skillLenth) + 1):
                Lenth = float(i)
                pX = self.char.npc.x - math.sin(self.cita) * Lenth
                pZ = self.char.npc.z + math.cos(self.cita) * Lenth
                pY = self.char.npc.y
                self.thisPartical(pX, pY, pZ, "largesmoke")
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

    def thisPartical(self, sx, sy, sz, partical):
        self.char.npc.world.spawnParticle(partical, sx, sy, sz, 0, 1, 0, 0, 10)


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

    def modify(self, timerId, ticks, repeat):
        self.timers[timerId] = [timerId, ticks, repeat]