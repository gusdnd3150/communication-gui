
from PySide6.QtWidgets import QTableWidgetItem, QMainWindow, QHeaderView
from PySide6.QtGui import QColor, QBrush
import sys
import os
import base64
import src.protocols.SendHandler as SendHandler
import traceback
from conf.skModule import *
from conf.sql.SystemQueryString import *
from ui.ui_direct import Ui_Direct

class Direct(QMainWindow):
    saveSkWindow = None
    initData = None
    byteData = bytearray()


    def __init__(self, initData):
        super(Direct, self).__init__()
        self.initData = initData
        self.ui = Ui_Direct()
        self.ui.setupUi(self)
        self.setWindowTitle('메시지 전송')
        self.setEvent()


    def setEvent(self):
        self.ui.dir_send.clicked.connect(self.sendBytes)
        self.ui.dir_string.clicked.connect(self.addString)
        self.ui.dir_float.clicked.connect(self.addFloat)
        self.ui.dir_int.clicked.connect(self.addInt)
        self.ui.dir_double.clicked.connect(self.addDouble)
        self.ui.dir_decimal.clicked.connect(self.addDecimal)
        self.ui.dir_decimals.clicked.connect(self.addDecimals)
        
        self.ui.dir_buffer.setReadOnly(True) # 수정불가



    def addString(self):
        try:
            data = self.ui.dir_input.toPlainText()
            if data is None or data != '':
                self.byteData.extend(data.encode('utf-8'))
                self.ui.dir_buffer.setPlainText(str(self.byteData))
        except:
            logger.error(f'sendBytes error : {traceback.format_exc()}')

    def addFloat(self):
        try:
            print('addString')
        except:
            logger.error(f'sendBytes error : {traceback.format_exc()}')

    def addInt(self):
        try:
            print('addString')
        except:
            logger.error(f'sendBytes error : {traceback.format_exc()}')
    def addDouble(self):
        try:
            print('addString')
        except:
            logger.error(f'sendBytes error : {traceback.format_exc()}')

    def addDecimal(self):
        try:
            print('addString')
        except:
            logger.error(f'sendBytes error : {traceback.format_exc()}')

    def addDecimals(self):
        try:
            print('addString')
        except:
            logger.error(f'sendBytes error : {traceback.format_exc()}')

    def sendBytes(self):
        skId = self.ui.dir_sk.currentText()
        data = self.ui.dir_buffer.toPlainText()
        try:
            print(f'data : {data}, skId : {skId}')
            # logger.info(f'Direct.sendMsg() skId: {skId}, msgId:{self.msgId} resultObj : {resultObj}')
            # SendHandler.sendSkIdBytes(self,skId)


            self.byteData.clear()
            self.ui.dir_buffer.clear()
        except:
            self.byteData.clear()
            self.ui.dir_buffer.clear()
            self.ui.dir_buffer.setPlainText(f'exception {traceback.format_exc()}')
