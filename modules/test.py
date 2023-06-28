import threading
import time

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
        self.Timer = MyTimerThreading(self.timer)

        # define timerId
        self.timerAlarm = 1
        self.timerDuration = 2
        self.timerInterval = 3
        self.timerHang = 4

        self.Timer.create(self.timerAlarm, 2, False)
        self.Timer.create(self.timerDuration, 3, False)
        self.Timer.create(self.timerInterval, 7, False)
        self.Timer.create(self.timerHang, 5, False)

        self.GoldSword = _char.npc.world.createItem("minecraft:golden_sword", 0, 1)
        self.Air = _char.npc.world.createItem("minecraft:air", 0, 1)

    def interact(self):
        pass

    def timer(self, timer_id):
        self.skill_rage(timer_id)

    def target(self):
        self.Timer.start(self.timerAlarm)
        self.char.npc.say("alarm")
        # do something

    def targetLost(self):
        self.Timer.start(self.timerHang)
        # do something

    def strengthen(self):
        self.char.npc.stats.melee.setStrength(6)
        self.char.npc.stats.melee.setDelay(4)
        self.char.npc.inventory.setLeftHand(self.GoldSword)
        self.circleExplode(1, "lava")

    def recover(self):
        self.char.npc.stats.melee.setStrength(7)
        self.char.npc.stats.melee.setDelay(16)
        self.char.npc.inventory.setLeftHand(self.Air)

    def skill_rage(self, timer_id):
        # Alarm ends
        # self.Timer.finish(timer_id)
        if timer_id == self.timerAlarm:
            self.char.npc.say("start")
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
            self.char.npc.say("stop")
            if self.char.npc.isAttacking():
                self.Timer.start(self.timerInterval)
            self.recover()

        # Hang ends
        if timer_id == self.timerHang:
            if not self.char.npc.isAttacking():
                self.recover()
                self.Timer.stopAll()

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


class MyTimerThreading:
    def __init__(self, callback):
        self.callback = callback
        self.map = {}
        self.timers = []
        self.isRunning = []
        self.alive = {}
        self.sems_start = []
        self.workertid = []
        self.tid = 0

    def create(self, timerId, seconds, repeat=False):
        self.timers.append([timerId, seconds, repeat])
        self.alive[self.tid] = True
        self.sems_start.append(threading.Semaphore(0))
        self.isRunning.append(False)
        self.workertid.append(self.tid)
        self.map[timerId] = len(self.timers) - 1

        thread = threading.Thread(target=self.timer_thread, args=(self.tid, timerId))
        thread.daemon = True
        thread.start()

        self.tid += 1

    def start(self, timerId):
        timerId = self.map[timerId]
        status = self.alive.get(self.workertid[timerId])
        # worker thread deleted
        if status is None:
            self.workertid[timerId] = self.tid
            self.alive[self.tid] = True
            thread = threading.Thread(
                target=self.timer_thread, args=(self.tid, timerId)
            )
            thread.daemon = True
            thread.start()

            self.tid += 1

        else:
            if self.isRunning[timerId] is False:
                self.sems_start[timerId].release()
                self.isRunning[timerId] = True

    def stop(self, timerId):
        timerId = self.map[timerId]
        del self.alive[self.workertid[timerId]]
        self.isRunning[timerId] = False

    def modify(self, timerId, seconds, repeat):
        timerId = self.map[timerId]
        self.timers[timerId] = [seconds, repeat]
        pass

    def stopAll(self):
        for timerId, sec, rep in self.timers:
            self.stop(timerId)

    def timer_thread(self, tid, timerId):
        while True:
            # wait for lock
            timer_id = self.map[timerId]
            self.sems_start[timer_id].acquire()

            time.sleep(self.timers[timer_id][1])

            status = self.alive.get(tid)
            if status is None:
                return

            # repeat
            if self.timers[timer_id][2]:
                self.sems_start[timer_id].release()
            else:
                self.isRunning = False

            self.callback(timerId)
