from PySide6.QtWidgets import QWidget, QSizePolicy
from PySide6.QtGui import QPainter, QColor, QPen, QFont
from PySide6.QtCore import Qt


class RadialGauge(QWidget):
    def __init__(self, title, min_val, max_val, unit, color, invert=False):
        super().__init__()

        self.title = title
        self.min = min_val
        self.max = max_val
        self.unit = unit
        self.color = QColor(color)
        self.value = min_val
        self.invert = invert

        # 🔒 HARD SIZE LOCK (prevents overlap forever)
        self.setFixedSize(180, 180)

        self.setSizePolicy(
            QSizePolicy.Fixed,
            QSizePolicy.Fixed
        )

    def set_value(self, v):
        self.value = max(self.min, min(v, self.max))
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        size = self.width()
        center = size / 2
        radius = center - 18
        thickness = 14

        p.translate(center, center)

        # ===== BACKGROUND ARC =====
        bg_pen = QPen(QColor("#1e293b"), thickness)
        bg_pen.setCapStyle(Qt.RoundCap)
        p.setPen(bg_pen)
        p.drawArc(
            -radius, -radius,
            radius * 2, radius * 2,
            225 * 16, 270 * 16
        )

        # ===== VALUE ARC =====
        ratio = (self.value - self.min) / (self.max - self.min)
        if self.invert:
            ratio = 1 - ratio

        angle = int(270 * ratio)

        fg_pen = QPen(self.color, thickness)
        fg_pen.setCapStyle(Qt.RoundCap)
        p.setPen(fg_pen)
        p.drawArc(
            -radius, -radius,
            radius * 2, radius * 2,
            225 * 16, -angle * 16
        )

        # ===== VALUE =====
        p.setPen(QColor("#e5e7eb"))
        p.setFont(QFont("Segoe UI", 26, QFont.Bold))
        p.drawText(
            -center, -12,
            size, 40,
            Qt.AlignCenter,
            f"{int(self.value)}"
        )

        # ===== UNIT =====
        p.setFont(QFont("Segoe UI", 10))
        p.drawText(
            -center, 18,
            size, 20,
            Qt.AlignCenter,
            self.unit
        )

        # ===== TITLE =====
        p.setFont(QFont("Segoe UI", 11))
        p.setPen(QColor("#7dd3fc"))
        p.drawText(
            -center, radius - 10,
            size, 20,
            Qt.AlignCenter,
            self.title
        )

        p.end()
