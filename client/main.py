import sys
from PySide6.QtWidgets import QApplication
from app import App

app = QApplication(sys.argv)
w = App()
w.show()
sys.exit(app.exec())
