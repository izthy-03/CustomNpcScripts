import threading
import time


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

            for child in nowSkill.child:
                if child.skillCond():
                    time.sleep(child.skillPrev())
                    if child.skillCond():
                        child.skillEffect()
                        time.sleep(child.skillDuration())
                        nowSkill = child
                    else:
                        nowSkill = self.root
                        self.reset()
                    break
