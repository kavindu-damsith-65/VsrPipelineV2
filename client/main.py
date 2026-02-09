import sys, os
from PySide6.QtWidgets import QApplication
from realnet_ui import RealNet

app = QApplication(sys.argv)

base = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(base, "theme.qss")) as f:
    app.setStyleSheet(f.read())

w = RealNet()
w.show()
sys.exit(app.exec())
