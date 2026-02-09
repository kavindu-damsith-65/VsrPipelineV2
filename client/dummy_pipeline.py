import cv2
import time

class DummyPipeline:
    def __init__(self):
        self.cost = 8

    def set_model(self, name):
        self.cost = {"Fast": 6, "Medium": 12, "Heavy": 24}[name]

    def run(self, frame):
        t0 = time.perf_counter()
        time.sleep(self.cost / 1000)
        out = cv2.resize(frame, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)
        latency = (time.perf_counter() - t0) * 1000
        return out, latency
