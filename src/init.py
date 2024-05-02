import sys
import os

program_path = sys.argv[0]
program_directory = os.path.dirname(program_path)


from PySide6 import QtWidgets
from PySide6.QtUiTools import QUiLoader

from src.component.settings.Settings import Settings
from conf.logconfig import logger

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

program_path = sys.argv[0]
program_directory = os.path.dirname(program_path)


# logger.info(resource_path('test.ui'))
# form = resource_path('test.ui')


# 네이밍
# 1. btn_?, popup_?, input_?,

class InitClass():

    mainLayOut = None
    popup = None # 설정 팝업
    saveSkWindow = None
    qLoader = None
    list_table = None

    def __init__(self):
        logger.info('init UI start')

        self.qLoader = QUiLoader()
        app = QtWidgets.QApplication(sys.argv)

        #메인창
        self.mainLayOut = self.qLoader.load(resource_path('main.ui'), None)
        self.mainLayOut.setWindowTitle('application')
        self.mainLayOut.btn_settings.clicked.connect(self.settings)
        self.mainLayOut.show()
        # 설정팝업
        self.popup = Settings()
        self.setEvent()
        self.setInitData()
        app.exec()

    def setEvent(self):
        # self.popup
        # self.mainLayOut
        logger.info('tset')

        # list_table =

    def setInitData(self):
        logger.info('load Init Data')
        program_directory+'\json\*.json'



    def settings(self):
        logger.info('tesst')
        if self.popup.instance.isVisible():
            self.popup.instance.hide()
        else:
            self.popup.instance.show()


    def addTableRow(self, items):
        logger.info('test')
