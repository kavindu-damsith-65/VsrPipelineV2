from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox
)
from PySide6.QtCore import QTimer
from PySide6.QtGui import QImage, QPainter
from stream import StreamReceiver
from model import ModelManager
from pipeline import Pipeline
from metrics import StageTimer, FPSCounter

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ForkNet Client – SR Stream")
        self.resize(1100, 700)

        self.video = QLabel()
        self.video.setMinimumSize(800, 450)

        self.model_box = QComboBox()
        self.model_box.addItems(["ForkNet", "Bicubic"])

        self.stats = QLabel()

        side = QVBoxLayout()
        side.addWidget(QLabel("Model"))
        side.addWidget(self.model_box)
        side.addWidget(self.stats)

        layout = QHBoxLayout(self)
        layout.addWidget(self.video, 3)
        layout.addLayout(side, 1)

        # core
        self.timer = StageTimer()
        self.fps = FPSCounter()
        self.model = ModelManager()
        self.pipe = Pipeline(self.model)
        self.rx = StreamReceiver(426, 240)

        self.model_box.currentTextChanged.connect(self.model.set)

        self.qt = QTimer()
        self.qt.timeout.connect(self.update)
        self.qt.start(1)

    def update(self):
        self.timer.start("decode")
        frame = self.rx.read()
        self.timer.stop("decode")

        if frame is None:
            return

        self.timer.start("sr")
        out = self.pipe.process(frame)
        self.timer.stop("sr")

        self.fps.tick()

        img = QImage(out.data, out.shape[1], out.shape[0],
                     3*out.shape[1], QImage.Format_RGB888)
        pix = img.scaled(self.video.size())
        self.video.setPixmap(pix)

        self.stats.setText(
            f"FPS: {self.fps.fps():.1f}\n"
            f"Decode: {self.timer.times['decode']:.2f} ms\n"
            f"SR: {self.timer.times['sr']:.2f} ms"
        )
