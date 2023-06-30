import math
import threading
import time

# 定义测试npc
test = None


# hook必须暴露在外，曲折实现封装
def init(c):
    # 实例化
    global test
    test = Item(c)


def interact(c):
    global test
    test.interact(c)


class Item:
    def __init__(self, _item):
        self.item = _item
        self.SkillTree = SkillTree()

        # self.setItemDamage(1)
        # self.setTexture(1,"magistuarmory:wood_stylet")
        # self.setCustomName("§1悔罪之槌")

        self.SkillTree.regReset(None)

        self.isUsing = False

        self.Lenth = 6.0
        self.Width = 1.0

        self.started = False

        # self.sX1 = self.char.player.x
        # self.sZ1 = self.char.player.z
        # self.sX2 = self.char.player.x
        # self.sZ2 = self.char.player.z
        # self.sX3 = self.char.player.x
        # self.sZ3 = self.char.player.z
        # self.sX4 = self.char.player.x
        # self.sZ4 = self.char.player.z
        # self.sY = self.char.player.y
        # self.cita = self.char.player.rotation

        # self.skillDamage = self.char.player.getMaxHealth()

        # self.SkillTree.regSkill("Alarm", lambda: None, lambda: True, lambda: 2)
        self.SkillTree.regSkill(
            "Prepare",
            self.prepare,
            lambda: self.isUsing,
            lambda: 0,
            lambda: 1,
        )
        self.SkillTree.regSkill(
            "Smite", self.smite, lambda: True, lambda: 0, lambda: 0, "Prepare"
        )
        self.SkillTree.regSkill(
            "Cooldown", self.toZero, lambda: True, lambda: 2, lambda: 0, "Smite"
        )
        # self.SkillTree.startCycle()

    def interact(self, char):
        self.char = char
        self.sX1 = self.char.player.x
        self.sZ1 = self.char.player.z
        self.sX2 = self.char.player.x
        self.sZ2 = self.char.player.z
        self.sX3 = self.char.player.x
        self.sZ3 = self.char.player.z
        self.sX4 = self.char.player.x
        self.sZ4 = self.char.player.z
        self.sY = self.char.player.y
        self.cita = self.char.player.rotation

        self.skillDamage = self.char.player.getMaxHealth()

        self.isUsing = True

        if not self.started:
            self.SkillTree.startCycle()
            self.started = True

    def toZero(self):
        self.isUsing = False

    def prepare(self):
        self.cita = self.char.player.rotation
        if abs(self.cita) >= 360:
            self.cita = self.cita % 360
        self.cita = self.cita * math.pi / 180
        for i in range(1, int(self.Lenth) + 1):
            Lenth = float(i)
            pX = self.char.player.x - math.sin(self.cita) * Lenth
            pZ = self.char.player.z + math.cos(self.cita) * Lenth
            pY = self.char.player.y + 0.5
            self.thisPartical(pX, pY, pZ, "cloud")
        self.sX1 = self.char.player.x - math.cos(self.cita) * self.Width
        self.sZ1 = self.char.player.z - math.sin(self.cita) * self.Width
        self.sX2 = self.char.player.x + math.cos(self.cita) * self.Width
        self.sZ2 = self.char.player.z + math.sin(self.cita) * self.Width
        self.sX3 = self.sX1 - math.sin(self.cita) * self.Lenth
        self.sZ3 = self.sZ1 + math.cos(self.cita) * self.Lenth
        self.sX4 = self.sX2 - math.sin(self.cita) * self.Lenth
        self.sZ4 = self.sZ2 + math.cos(self.cita) * self.Lenth
        self.sY = self.char.player.y

    def smite(self):
        for entity in self.char.player.world.getNearbyEntities(
            self.char.player.pos, 9, 1000
        ):
            if entity != self.char.player:
                x = entity.x
                y = entity.y
                z = entity.z
                a1 = (self.sX2 - self.sX1, self.sZ2 - self.sZ1)
                b1 = (x - self.sX1, z - self.sZ1)
                t1 = a1[0] * b1[1] - a1[1] * b1[0]
                a2 = (self.sX4 - self.sX3, self.sZ4 - self.sZ3)
                b2 = (x - self.sX3, z - self.sZ3)
                t2 = a2[0] * b2[1] - a2[1] * b2[0]
                a3 = (self.sX3 - self.sX2, self.sZ3 - self.sZ2)
                b3 = (x - self.sX2, z - self.sZ2)
                t3 = a3[0] * b3[1] - a3[1] * b3[0]
                a4 = (self.sX1 - self.sX4, self.sZ1 - self.sZ4)
                b4 = (x - self.sX4, z - self.sZ4)
                t4 = a4[0] * b4[1] - a4[1] * b4[0]
                if t1 * t2 <= 0 and t3 * t4 >= 0 and (y - self.sY) <= 2:
                    entity.damage(self.skillDamage)
                    entity.addPotionEffect(2, 3, 4, False)
        for i in range(1, int(self.Lenth) + 1):
            Lenth = float(i)
            pX = self.char.player.x - math.sin(self.cita) * Lenth
            pZ = self.char.player.z + math.cos(self.cita) * Lenth
            pY = self.char.player.y
            self.thisPartical(pX, pY, pZ, "largesmoke")

    def circleExplode(self, radius, particle):
        thisX = self.char.player.getX()
        thisY = self.char.player.getY()
        thisZ = self.char.player.getZ()
        for i in range(0, 360, 5):
            rad = i * math.pi / 180
            dx = math.cos(rad)
            dz = math.sin(rad)
            self.char.player.world.spawnParticle(
                particle, thisX, thisY + 1, thisZ, dx, 0, dz, 0.01, 5
            )

    def thisPartical(self, sx, sy, sz, partical):
        self.char.player.world.spawnParticle(partical, sx, sy, sz, 0, 1, 0, 0, 10)


class SkillNode:
    def __init__(self, skillName, skillEffect, skillCond, skillPrev, skillDuration):
        self.skillName = skillName
        self.skillEffect = skillEffect
        self.skillCond = skillCond
        self.skillPrev = skillPrev
        self.skillDuration = skillDuration

        self.child = []


class SkillTree:
    def __init__(self):
        self.root = SkillNode("", None, None, None, None)

    def startCycle(self):
        thread = threading.Thread(target=self.thread_skill)
        thread.daemon = True
        thread.start()

    def regSkill(
        self, skillName, skillEffect, skillCond, skillPrev, skillDuration, deriveFrom=""
    ):
        newSkill = SkillNode(
            skillName, skillEffect, skillCond, skillPrev, skillDuration
        )
        derive = self.find(self.root, deriveFrom)
        if derive is not None:
            derive.child.append(newSkill)
            return True
        else:
            return False

    def regReset(self, resetFunc):
        self.reset = resetFunc

    def find(self, node, name):
        if node.skillName == name:
            return node
        else:
            for child in node.child:
                found = self.find(child, name)
                if found is not None:
                    return found
        return None

    def thread_skill(self):
        nowSkill = self.root
        while True:
            # reach leaf
            if 0 == len(nowSkill.child):
                nowSkill = self.root
            flag = False
            for child in nowSkill.child:
                if child.skillCond():
                    time.sleep(child.skillPrev())
                    if child.skillCond():
                        child.skillEffect()
                        time.sleep(child.skillDuration())
                        if child.skillCond():
                            nowSkill = child
                        else:
                            nowSkill = self.root
                            self.reset()
                    else:
                        nowSkill = self.root
                        self.reset()
                    flag = True
                    break

            if not flag:
                nowSkill = self.root
