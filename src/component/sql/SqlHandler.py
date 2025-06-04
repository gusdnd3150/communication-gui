import struct
from PySide6.QtWidgets import QTableWidgetItem, QMainWindow, QHeaderView
import sys
import os
import base64
import traceback
from conf.skModule import *
from conf.sql.SystemQueryString import *
from ui.ui_sqlHandler import Ui_MainWindow

class SqlHandler(QMainWindow):

    initData = None

    def __init__(self, initData):
        super(SqlHandler, self).__init__()
        self.initData = initData
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('쿼리 실행')
        self.setEvent()

    def setEvent(self):
        self.ui.sql_excute.clicked.connect(self.sqlExcute)

    def sqlExcute(self):
        try:
            text = self.ui.sql_text.toPlainText()
            if text:
                queryExecute(text)
        except:
            logger.error(f'sqlExcute error : {traceback.format_exc()}')
