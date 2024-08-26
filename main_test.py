import sys
sys.path.append('.')
from PySide6.QtWidgets import QApplication, QMainWindow
from src.init import InitClass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = InitClass()
    window.show()
    sys.exit(app.exec())
