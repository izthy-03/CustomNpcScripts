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

def damaged(c):
    global test
    test.damaged()

def collide(c):
    global test
    test.collide()

class Entity:
    def __init__(self, _char):
        self.char = _char
        self.char.npc.say("Initialized!")
        self.Timer = MyTimer(_char.npc.getTimers())

        # define timerId
        self.timerEarthBurnCooldown = 1
        self.timerAlarmEarthBurn = 2
        self.timerFireRingCooldown = 3
        self.timerAlarmFireRing = 4
        self.timerPhysicalCooldown = 5
        self.timerAlarmCounter = 6
        self.timerCounter = 7
        self.timerAlarmDash = 8
        self.timerDash = 9
        self.timerCheck = 10

        self.Timer.add(self.timerEarthBurnCooldown, 100, False)
        self.Timer.add(self.timerAlarmEarthBurn, 10, False)
        self.Timer.add(self.timerFireRingCooldown, 100, False)
        self.Timer.add(self.timerAlarmFireRing, 10, False)
        self.Timer.add(self.timerPhysicalCooldown, 120, False)
        self.Timer.add(self.timerAlarmCounter, 40, False)
        self.Timer.add(self.timerCounter, 10, False)
        self.Timer.add(self.timerAlarmDash, 10, False)
        self.Timer.add(self.timerDash,10, False)
        self.Timer.add(self.timerCheck, 107, True)

        self.Timer.stop(self.timerCheck)
        self.Timer.start(self.timerCheck)

        self.skillRange = 5


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
        self.skillWidth = 2.0

        self.DashRotation = 0.0

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
        self.Timer.start(self.timerEarthBurnCooldown)
        self.Timer.start(self.timerPhysicalCooldown)

    def targetLost(self):
        # 5秒待机，防止切换仇恨时技能重置
        # self.Timer.start(self.timerHang)
        pass

    def skill(self, timer_id):
        if timer_id == self.timerEarthBurnCooldown:
            self.prepareEarthBurn()
            self.Timer.start(self.timerAlarmEarthBurn)
        
        if timer_id == self.timerAlarmEarthBurn:
            self.EarthBurn()
            ranFireRing = random.randint(80, 120)
            self.Timer.modify(self.timerFireRingCooldown, ranFireRing, False)
            self.Timer.start(self.timerFireRingCooldown)

        if timer_id == self.timerFireRingCooldown:
            self.prepareFireRing()
            self.Timer.start(self.timerAlarmFireRing)

        if timer_id == self.timerAlarmFireRing:
            self.FireRing()
            ranEarthBurn = random.randint(80, 120)
            self.Timer.modify(self.timerEarthBurnCooldown, ranEarthBurn, False)
            self.Timer.start(self.timerEarthBurnCooldown)
        
        if timer_id == self.timerPhysicalCooldown:
            if self.char.npc.getAttackTarget().getPos().distanceTo(self.char.npc.getPos()) <= 3:
                self.Defend()
                self.Timer.start(self.timerAlarmCounter)
            if self.char.npc.getAttackTarget().getPos().distanceTo(self.char.npc.getPos()) > 3:
                self.AlarmDash()
                self.Timer.start(self.timerAlarmDash)
        
        if timer_id == self.timerAlarmCounter:
            self.toNormal()
            ranPhysical = random.randint(100, 160)
            self.Timer.modify(self.timerPhysicalCooldown, ranPhysical, False)
            self.Timer.start(self.timerPhysicalCooldown)
        
        if timer_id == self.timerCounter:
            self.Counter()
            self.toNormal()
            ranPhysical = random.randint(100, 160)
            self.Timer.modify(self.timerPhysicalCooldown, ranPhysical, False)
            self.Timer.start(self.timerPhysicalCooldown)
        
        if timer_id == self.timerAlarmDash:
            self.Dash()
            self.Timer.start(self.timerDash)

        if timer_id == self.timerDash:
            self.toNormal()
            ranPhysical = random.randint(100, 160)
            self.Timer.modify(self.timerPhysicalCooldown, ranPhysical, False)
            self.Timer.start(self.timerPhysicalCooldown)

    def prepareEarthBurn(self):
        # self.char.npc.playAnimation(0)
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
        for i in range(1, int(self.skillLenth) + 1):
            Lenth = float(i)
            pX = self.char.npc.x - math.cos(self.cita) * 1.0 - math.sin(self.cita) * Lenth
            pZ = self.char.npc.z - math.sin(self.cita) * 1.0 + math.cos(self.cita) * Lenth
            pY = self.char.npc.y + 0.5
            self.thisPartical(pX, pY, pZ, "cloud")
        for i in range(1, int(self.skillLenth) + 1):
            Lenth = float(i)
            pX = self.char.npc.x + math.cos(self.cita) * 1.0 - math.sin(self.cita) * Lenth
            pZ = self.char.npc.z + math.sin(self.cita) * 1.0 + math.cos(self.cita) * Lenth
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



    def EarthBurn(self):
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
                    entity.setBurning(20)
                    entity.addPotionEffect( 7, 1, 0, False)
        for i in range(1, int(self.skillLenth) + 1):
            Lenth = float(i)
            pX = self.char.npc.x - math.sin(self.cita) * Lenth
            pZ = self.char.npc.z + math.cos(self.cita) * Lenth
            pY = self.char.npc.y
            self.thisPartical(pX, pY, pZ, "lava")
        for i in range(1, int(self.skillLenth) + 1):
            Lenth = float(i)
            pX = self.char.npc.x - math.cos(self.cita) * 1.0 - math.sin(self.cita) * Lenth
            pZ = self.char.npc.z - math.sin(self.cita) * 1.0 + math.cos(self.cita) * Lenth
            pY = self.char.npc.y + 0.5
            self.thisPartical(pX, pY, pZ, "lava")
        for i in range(1, int(self.skillLenth) + 1):
            Lenth = float(i)
            pX = self.char.npc.x + math.cos(self.cita) * 1.0 - math.sin(self.cita) * Lenth
            pZ = self.char.npc.z + math.sin(self.cita) * 1.0 + math.cos(self.cita) * Lenth
            pY = self.char.npc.y + 0.5
            self.thisPartical(pX, pY, pZ, "lava")

    def prepareFireRing(self):
        self.circle(self.skillRange, "largesmoke")

    def FireRing(self):
        thisPos = self.char.npc.getPos()
        players = self.char.npc.world.getNearbyEntities(thisPos, 12, 1000)
        thisY = self.char.npc.getY()
        # self.char.npc.say("my Y = " + str(thisY))
        self.circle(self.skillRange, "flame")
        self.circle(self.skillRange + 1, "flame")
        self.circle(self.skillRange + 2, "flame")
        self.circle(self.skillRange + 3, "flame")
        self.circle(self.skillRange + 4, "flame")
        for player in players:
            coordY = player.getY()
            # name = player.getName()
            # self.char.npc.say(name + " y = " + str(coordY))
            distance = player.getPos().distanceTo(thisPos)
            if coordY - thisY <= 2 and distance >= self.skillRange and distance <= self.skillRange + 4:
                player.setBurning(20)
                player.addPotionEffect( 7, 1, 1, False)
    
    def damaged(self):
        if self.Timer.isRunning[self.timerAlarmCounter]:
            self.damage = 0
            self.Timer.stop(self.timerAlarmCounter)
            self.Timer.start(self.timerCounter)
        if self.Timer.isRunning[self.timerCounter]:
            self.damage = 0


    def Defend(self):
        self.char.npc.world.playSoundAt(self.char.npc.getPos(), 'minecraft:item.armor.equip_iron', 1, 1)
        self.char.npc.getAi().setWalkingSpeed(0)
        self.circleExplode(1,"largesmoke")

    def Counter(self):
        targets = self.char.npc.world.getNearbyEntities(self.char.npc.getPos(), 3, 1000)
        for target in targets:
            if target != self.char.npc:
                target.damage(20)

    def AlarmDash(self):
        self.char.npc.getAi().setWalkingSpeed(0)
        self.circleExplode(1,"cloud")
        self.DashRotation = self.char.npc.getRotation()

    def Dash(self):
        self.char.npc.knockback(4, self.DashRotation)

    def collide(self):
        if self.Timer.isRunning[self.timerDash]:
            dashes = self.char.npc.world.getNearbyEntities(self.char.npc.getPos(), 1, 1000)
            for dash in dashes:
                if dash != self.char.npc:
                    dash.damage(16)
                    dash.setBurning(5)
            
        

    def toNormal(self):
        self.char.npc.getAi().setWalkingSpeed(5)

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
            py = thisY + 0.5
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
                particle, thisX, thisY + 1, thisZ, dx, 0, dz, 0.01, 5
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