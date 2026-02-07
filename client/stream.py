import subprocess
import numpy as np

class StreamReceiver:
    def __init__(self, width, height, url="udp://127.0.0.1:5001"):
        self.w = width
        self.h = height

        self.proc = subprocess.Popen(
            [
                "ffmpeg",
                "-hwaccel", "cuda",
                "-i", url,
                "-f", "rawvideo",
                "-pix_fmt", "rgb24",
                "-"
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            bufsize=10**8
        )

    def read(self):
        size = self.w * self.h * 3
        raw = self.proc.stdout.read(size)
        if len(raw) != size:
            return None
        return np.frombuffer(raw, np.uint8).reshape(self.h, self.w, 3)
