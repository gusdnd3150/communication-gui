import traceback

from PySide6.QtUiTools import QUiLoader

from conf.logconfig import logger

class SaveSocketPopup():

    instance = None  # 위젯

    def __init__(self,filePath, parent=None):
        self.instance = QUiLoader().load(filePath, None)
        self.instance.setWindowTitle('소켓 추가')
        # self.instance.show()


    def setForm(self, formIndex):
        try:
            logger.info('setForm')
            if(formIndex == 0):
                logger.info('Form SK table')
            elif(formIndex == 1):
                logger.info('Form SK_MSG table')
            else:
                logger.info('None condition')

        except:
            traceback.print_stack()


    def clearForm(self):
        logger.info('clearForm')


