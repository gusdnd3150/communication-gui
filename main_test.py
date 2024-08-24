
import sys
sys.path.append('.')
from conf.logconfig import logger
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Qt
from src.init_test import InitClass

from src.component.settings.Settings import Settings

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = InitClass()
    window.show()
    sys.exit(app.exec())