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


# 네이밍
# 1. btn_?, popup_?, input_?,

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
        self.mainLayOut = self.qLoader.load(resource_path('views/main.ui'), None)
        self.mainLayOut.setWindowTitle('통신테스터')
        self.mainLayOut.btn_settings.clicked.connect(self.addInt)
        self.mainLayOut.show()

        #팝업1
        self.popup = self.qLoader.load(resource_path('views/test.ui'), None)
        self.popup.setWindowTitle('설정')

        app.exec()


    def runProccess(self):
        print('test')


    def addInt(self):
        print('test')
        if self.popup.isVisible():
            self.popup.hide()
        else:
            self.popup.show()

