import threading
import time


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
            if not self.isRunning[timerId]:
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
