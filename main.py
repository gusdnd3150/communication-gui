import sys, os
sys.path.append('.')
from PySide6.QtWidgets import QApplication
from src.init import InitClass

if __name__ == '__main__':

    print(f'sys.implementation.name  :: {sys.implementation.name}')
    print(os.getcwd())
    print(os.path.abspath('.'))

    app = QApplication(sys.argv)
    window = InitClass()
    window.show()
    sys.exit(app.exec())
