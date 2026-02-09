from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout,
    QGroupBox, QRadioButton,
    QScrollArea
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QImage, QPixmap
import cv2

from dummy_video import DummyVideo
from dummy_pipeline import DummyPipeline
from metrics import Metrics
from gauges import RadialGauge


class RealNet(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("RealNet Client")
        self.resize(1600, 900)
        self.setMinimumSize(1280, 720)

        # ================= TITLE =================
        title = QLabel("RealNet – Super Resolution Client")
        title.setObjectName("Title")

        # ================= VIDEO =================
        self.video = QLabel()
        self.video.setMinimumSize(640, 360)
        self.video.setAlignment(Qt.AlignCenter)
        self.video.setStyleSheet("background:#020617; border-radius:14px;")

        # ================= CONTROLS =================
        self.play_btn = QPushButton("▶ Play")
        self.pause_btn = QPushButton("⏸ Pause")
        self.stop_btn = QPushButton("⏹ Stop")

        self.status = QLabel("● STOPPED")
        self.status.setStyleSheet("color:#ef4444; font-weight:bold;")

        ctrl = QHBoxLayout()
        ctrl.addWidget(self.play_btn)
        ctrl.addWidget(self.pause_btn)
        ctrl.addWidget(self.stop_btn)
        ctrl.addSpacing(20)
        ctrl.addWidget(self.status)
        ctrl.addStretch()

        # ================= PIPELINE =================
        self.pipeline = DummyPipeline()

        # ================= MODEL =================
        model_box = QGroupBox("Model")
        ml = QVBoxLayout()
        for m in ("Fast", "Medium", "Heavy"):
            r = QRadioButton(m)
            r.toggled.connect(lambda x, m=m: x and self.pipeline.set_model(m))
            ml.addWidget(r)
        ml.itemAt(0).widget().setChecked(True)
        model_box.setLayout(ml)

        # ================= VIDEO SOURCE =================
        self.video_src = DummyVideo("C:\PROGRAMMING\Fyp\VsrPipelineV2\client\4415029-sd_426_240_30fps (4).mp4")

        info = QLabel(
            f"Resolution: {self.video_src.width} × {self.video_src.height}\n"
            f"FPS: {self.video_src.fps}\n"
            f"Codec: {self.video_src.codec}\n"
            f"Bitrate: {self.video_src.bitrate}"
        )

        info_box = QGroupBox("Video Info")
        info_box.setLayout(QVBoxLayout())
        info_box.layout().addWidget(info)

        # ================= METRICS =================
        self.metrics = Metrics()

        self.stats = QLabel("FPS: 0\nLatency: 0 ms")
        stats_box = QGroupBox("Live Stats")
        stats_box.setLayout(QVBoxLayout())
        stats_box.layout().addWidget(self.stats)

        # ================= GAUGES =================
        self.fps_gauge = RadialGauge(
            "FPS", 0, 60, "fps", "#22c55e"
        )

        self.lat_gauge = RadialGauge(
            "Latency", 0, 1000, "ms", "#38bdf8", invert=True
        )

        perf_box = QGroupBox("Performance")
        perf_layout = QHBoxLayout()
        perf_layout.setSpacing(32)
        perf_layout.setContentsMargins(12, 12, 12, 12)
        perf_layout.addWidget(self.fps_gauge, alignment=Qt.AlignCenter)
        perf_layout.addWidget(self.lat_gauge, alignment=Qt.AlignCenter)
        perf_box.setLayout(perf_layout)

        # ================= SIDE PANEL =================
        side = QWidget()
        sl = QVBoxLayout(side)
        sl.addWidget(model_box)
        sl.addWidget(info_box)
        sl.addWidget(stats_box)
        sl.addWidget(perf_box)
        sl.addStretch()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(side)
        scroll.setMinimumWidth(380)
        scroll.setMaximumWidth(500)
        scroll.setStyleSheet("border:none;")

        # ================= MAIN =================
        main = QHBoxLayout()
        main.addWidget(self.video, 3)
        main.addWidget(scroll, 1)

        # ================= ROOT =================
        root = QVBoxLayout(self)
        root.setSpacing(8)
        root.setContentsMargins(16, 12, 16, 16)
        root.addWidget(title)
        root.addLayout(ctrl)
        root.addLayout(main)

        # ================= TIMER =================
        self.timer = QTimer()
        self.timer.setInterval(1)
        self.timer.timeout.connect(self.update_frame)

        self.play_btn.clicked.connect(self.start)
        self.pause_btn.clicked.connect(self.timer.stop)
        self.stop_btn.clicked.connect(self.timer.stop)

    def start(self):
        self.timer.start()
        self.status.setText("● LIVE")
        self.status.setStyleSheet("color:#22c55e; font-weight:bold;")

    def update_frame(self):
        frame = self.video_src.read()
        out, lat = self.pipeline.run(frame)
        self.metrics.tick(lat)

        rgb = cv2.cvtColor(out, cv2.COLOR_BGR2RGB)
        h, w, _ = rgb.shape
        img = QImage(rgb.data, w, h, 3 * w, QImage.Format_RGB888)

        pix = QPixmap.fromImage(img).scaled(
            self.video.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.video.setPixmap(pix)

        fps = self.metrics.fps()
        latency = self.metrics.latency_avg()

        self.stats.setText(
            f"FPS: {fps:.1f}\nLatency: {latency:.1f} ms"
        )

        self.fps_gauge.set_value(fps)
        self.lat_gauge.set_value(latency)
