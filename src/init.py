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

    mainLayOut = None
    popup = None
    qLoader = None

    def __init__(self):
        print('init UI start')
        # super().__init__()

        self.qLoader = QUiLoader()
        app = QtWidgets.QApplication(sys.argv)

        #메인창 화면 띄우기
        self.mainLayOut = self.qLoader.load(resource_path('test.ui'), None)
        self.mainLayOut.setWindowTitle('test')
        self.mainLayOut.btnInt.clicked.connect(self.addInt)
        self.mainLayOut.show()
        app.exec()


    def runProccess(self):
        print('test')


    def addInt(self):
        print('test')
        self.popup = self.qLoader.load(resource_path('test.ui'), None)
        self.popup.setWindowTitle('test')
        # self.popup.btnInt.clicked.connect(self.addInt)
        self.popup.show()