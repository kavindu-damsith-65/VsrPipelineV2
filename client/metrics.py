import time
from collections import deque

class StageTimer:
    def __init__(self):
        self.times = {}

    def start(self, name):
        self.times[name] = time.perf_counter_ns()

    def stop(self, name):
        self.times[name] = (time.perf_counter_ns() - self.times[name]) / 1e6

class FPSCounter:
    def __init__(self, window=30):
        self.ts = deque(maxlen=window)

    def tick(self):
        self.ts.append(time.time())

    def fps(self):
        if len(self.ts) < 2:
            return 0
        return (len(self.ts) - 1) / (self.ts[-1] - self.ts[0])
