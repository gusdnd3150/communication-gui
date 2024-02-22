import sys
import os

from PySide6 import QtWidgets
from PySide6.QtUiTools import QUiLoader

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# print(resource_path('test.ui'))
# form = resource_path('test.ui')
#
class InitClass():

    def __init__(self):
        print('init UI start')
        # super().__init__()

        loader = QUiLoader()
        app = QtWidgets.QApplication(sys.argv)
        window = loader.load(resource_path('test.ui'), None)
        window.setWindowTitle('test')
        window.show()
        app.exec()


    def runProccess(self):
        print('test')