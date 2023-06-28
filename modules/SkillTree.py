import threading
import time


class SkillNode:
    def __init__(self, skillName, skillEffect, skillCond, skillTime):
        self.skillName = skillName
        self.skillEffect = skillEffect
        self.skillCond = skillCond
        self.skillTime = skillTime

        self.child = []


class SkillTree:
    def __init__(self):
        self.root = SkillNode("", None, None)

    def startCycle(self):
        thread = threading.Thread(target=self.thread_skill)
        thread.daemon = True
        thread.start()

    def regSkill(self, skillName, skillEffect, skillCond, skillTime, deriveFrom=""):
        newSkill = SkillNode(skillName, skillEffect, skillCond, skillTime)
        derive = self.find(deriveFrom)
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

            for child in nowSkill.child:
                if child.skillCond():
                    time.sleep(child.skillTime())
                    if child.skillCond():
                        child.skillEffect()
                        nowSkill = child
                    else:
                        nowSkill = self.root
                        self.reset()
                    break
