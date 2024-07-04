import traceback

from PySide6.QtUiTools import QUiLoader

from conf.logconfig import logger
import sys, os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class SaveSocketPopup():
    instance = None  # 위젯

    def __init__(self, parent=None):

        path = resource_path('settings-saveSocket.ui')
        logger.info(f'path : {path}')

        self.instance = QUiLoader().load(path, None)
        self.instance.setWindowTitle('소켓 추가')
        # self.instance.show()


    def setForm(self, formIndex, jsonKey):
        try:
            logger.info('setForm')
            if(formIndex == 0): # 소켓테이블
                logger.info('Form SK table')
                logger.info(str(jsonKey))

            elif(formIndex == 1): # 소켓 in
                logger.info('Form SK_MSG table')
            else:
                logger.info('None condition')

        except:
            traceback.print_stack()


    def clearForm(self):
        logger.info('clearForm')


