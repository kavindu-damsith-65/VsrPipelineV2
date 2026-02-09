from PySide6.QtWidgets import QWidget, QSizePolicy
from PySide6.QtGui import QPainter, QColor, QPen, QPainterPath
from PySide6.QtCore import Qt

class CurvedChart(QWidget):
    def __init__(self, get_data, title, y_max, unit, color):
        super().__init__()
        self.get_data = get_data
        self.title = title
        self.y_max = y_max
        self.unit = unit
        self.color = QColor(color)

        self.setMinimumHeight(180)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def paintEvent(self, e):
        data = self.get_data()
        if len(data) < 2:
            return

        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        w, h = self.width(), self.height()
        m = 40

        p.fillRect(self.rect(), QColor("#020617"))

        axis = QPen(QColor("#334155"))
        p.setPen(axis)
        p.drawLine(m, m, m, h - m)
        p.drawLine(m, h - m, w - m, h - m)

        p.setPen(QColor("#64748b"))
        for i in range(5):
            y = h - m - i * (h - 2*m) / 4
            p.drawLine(m, y, w - m, y)
            p.drawText(5, y + 4, f"{int(i * self.y_max / 4)}")

        p.setPen(QColor("#7dd3fc"))
        p.drawText(m, 20, f"{self.title} ({self.unit})")

        pen = QPen(self.color, 2)
        p.setPen(pen)

        path = QPainterPath()
        step = (w - 2*m) / (len(data) - 1)

        def sy(v):
            return h - m - (min(v, self.y_max) / self.y_max) * (h - 2*m)

        path.moveTo(m, sy(data[0]))
        for i in range(1, len(data)):
            x = m + i * step
            path.lineTo(x, sy(data[i]))

        p.drawPath(path)
        p.end()
