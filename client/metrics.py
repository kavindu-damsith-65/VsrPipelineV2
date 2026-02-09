import time
from collections import deque

class Metrics:
    def __init__(self):
        self.ts = deque(maxlen=120)
        self.lat = deque(maxlen=120)

    def tick(self, latency):
        self.ts.append(time.time())
        self.lat.append(latency)

    def fps(self):
        if len(self.ts) < 2:
            return 0
        return (len(self.ts) - 1) / (self.ts[-1] - self.ts[0])

    def latency_avg(self):
        return sum(self.lat) / len(self.lat)

    def fps_history(self):
        return [self.fps()] * len(self.lat)

    def latency_history(self):
        return list(self.lat)
