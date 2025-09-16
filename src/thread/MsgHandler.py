
from PySide6.QtWidgets import QTableWidgetItem, QMainWindow, QHeaderView
from PySide6.QtGui import QColor, QBrush
import sys
import os
import src.protocols.SendHandler as SendHandler

import base64

program_path = sys.argv[0]
program_directory = os.path.dirname(program_path)
import traceback
from conf.skModule import *
# import conf.skModule as moduleData
from conf.sql.SystemQueryString import *
from ui.ui_handler import Ui_Handler

class MsgHandler():

    initData = None
    skRow = None
    contFlag = 'upd'
    msgId = None

    def __init__(self,ui):
        self.ui = ui
        self.setEvent()
        self.createMsgGrid(None,None)


    def setEvent(self):
        self.ui.main_btn_handle_search.clicked.connect(self.searchMsg)
        self.ui.main_btn_handle_send.clicked.connect(self.sendMsg)
        self.ui.main_btn_save_dt_val.clicked.connect(self.saveDefaultVal)
        self.ui.main_handle_search.textChanged.connect(self.searchMsg)




    def createMsgGrid(self, msg, mid):
        try:
            headers = ['MSG_ID', 'MSG_KEY_TYPE', 'MSG_KEY_VAL', 'MSG_DESC']
            self.ui.main_list_handle_msg.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            self.ui.main_list_handle_msg.setRowCount(0)  # Table의 행을 설정, list의 길이
            self.ui.main_list_handle_msg.setColumnCount(4)
            self.ui.main_list_handle_msg.setHorizontalHeaderLabels(headers)
            skList = selectQuery(selectSocketMSgList(msg, mid))
            for i, skItem in enumerate(skList):
                row_count = self.ui.main_list_handle_msg.rowCount()
                self.ui.main_list_handle_msg.insertRow(row_count)
                for j, hd in enumerate(headers):
                    if skItem.get(hd) is not None:
                        self.ui.main_list_handle_msg.setItem(row_count, j, QTableWidgetItem(str(skItem[hd])))
            self.ui.main_list_handle_msg.cellClicked.connect(self.selectMsgRow)
        except Exception as e:
            logger.error(f'createMsgGrid exception : {traceback.format_exc()}')


    def selectMsgRow(self,row, column):
        try:

            row_data = {}
            for column in range(self.ui.main_list_handle_msg.columnCount()):
                header_item = self.ui.main_list_handle_msg.horizontalHeaderItem(column)
                item = self.ui.main_list_handle_msg.item(row, column)
                row_data[header_item.text()] = item.text() if item else ""

            self.msgId = row_data['MSG_ID']
            self.createMsgDtGrid(row_data['MSG_ID'])
        except Exception as e :
            logger.error(f'selectMsgRow exception : {traceback.format_exc()} ')


    def searchMsg(self):
        try:
            self.createMsgGrid(self.ui.main_handle_search.text(),None)
        except Exception as e:
            logger.error(f'searchMsg exception : {traceback.format_exc()}')

    def createMsgDtGrid(self, msg):
        try:
            if msg is None or msg == '':
                return

            headers = ['MSG_DT_ORD', 'MSG_DT_VAL_ID', 'VALUE', 'VAL_TYPE', 'VAL_LEN']
            self.ui.main_list_handle_body.setRowCount(0)  # Table의 행을 설정, list의 길이
            self.ui.main_list_handle_body.setColumnCount(5)
            self.ui.main_list_handle_body.verticalHeader().setVisible(False)  # 행 번호 헤더 숨기기
            self.ui.main_list_handle_body.setHorizontalHeaderLabels(headers)
            skList = selectQuery(selectSocketMSgDtList(msg))
            print(skList)
            for i, skItem in enumerate(skList):
                row_count = self.ui.main_list_handle_body.rowCount()
                self.ui.main_list_handle_body.insertRow(row_count)
                for j, hd in enumerate(headers):
                    if skItem.get(hd) is not None:
                        item = QTableWidgetItem(str(skItem[hd]))
                        self.ui.main_list_handle_body.setItem(row_count, j, item)
                    if hd =='VALUE':
                        item = QTableWidgetItem(str(skItem['VAL_DESC']))
                        item.setBackground(QBrush(QColor(247, 243, 243)))  # 노란색 배경 설정
                        item.setForeground(QBrush(QColor(0, 0, 0)))
                        self.ui.main_list_handle_body.setItem(row_count, j, item)

        except Exception as e:
            logger.error(f'createMsgGrid exception: {traceback.format_exc()}')

    def sendMsg(self):
        try:
            row_count = self.ui.main_list_handle_body.rowCount()
            column_count = self.ui.main_list_handle_body.columnCount()
            headers = [self.ui.main_list_handle_body.horizontalHeaderItem(i).text() for i in range(column_count)]

            data = []
            resultObj = {}
            for row in range(row_count):
                row_data = {}
                for column in range(column_count):
                    item = self.ui.main_list_handle_body.item(row, column)
                    if item is not None:
                        row_data[headers[column]] = item.text()
                    else:
                        row_data[headers[column]] = None  # 셀이 비어있는 경우 None으로 처리
                data.append(row_data)

            for index, item in enumerate(data):
                if item['VAL_TYPE'] == 'STRING':
                    tempVal = str(item['VALUE'])
                    if tempVal is None:
                        tempVal =  str('').rjust(int(item['VALUE_LEN']), ' ')
                    resultObj[item['MSG_DT_VAL_ID']] = tempVal

                elif item['VAL_TYPE'] == 'INT' or item['VAL_TYPE'] == 'SHORT':
                    tempVal = int(item['VALUE'])
                    if tempVal is None:
                        tempVal = 0
                    resultObj[item['MSG_DT_VAL_ID']] = tempVal

                elif item['VAL_TYPE'] == 'DOUBLE' or item['VAL_TYPE'] == 'FLOAT':
                    tempVal = float(item['VALUE'])
                    if tempVal is None:
                        tempVal = 0.0
                    resultObj[item['MSG_DT_VAL_ID']] = tempVal

                elif item['VAL_TYPE'] == 'BYTE' or item['VAL_TYPE'] == 'BYTES':
                    tempVal = item['VALUE']
                    if tempVal is None:
                        tempVal = str('').rjust(int(item['VALUE_LEN']), ' ')
                    resultObj[item['MSG_DT_VAL_ID']] = tempVal

                elif item['VAL_TYPE'] == 'BASE64_DECMALS':
                    test = item['VALUE']
                    numbers = list(map(int, test.split()))
                    byte_array = bytearray(numbers)
                    base64_encoded = base64.b64encode(byte_array)
                    resultObj[item['MSG_DT_VAL_ID']] = base64_encoded.decode('utf-8')

            skId = self.ui.main_combo_sk_list.currentText()

            logger.info(f'Handler.sendMsg() skId: {skId}, msgId:{self.msgId} resultObj : {resultObj}')
            SendHandler.sendSkId(self,skId,self.msgId,resultObj)
        except:
            logger.error(f'sendMsg error : {traceback.format_exc()}')


    def saveDefaultVal(self):
        try:
            logger.info(f'saveDefaultVal')
            row_count = self.ui.main_list_handle_body.rowCount()
            column_count = self.ui.main_list_handle_body.columnCount()
            headers = [self.ui.main_list_handle_body.horizontalHeaderItem(i).text() for i in range(column_count)]

            data = []
            resultObj = {}
            for row in range(row_count):
                row_data = {}
                for column in range(column_count):
                    item = self.ui.main_list_handle_body.item(row, column)
                    row_data[headers[column]] = item.text()
                    # if item is not None:
                    #     row_data[headers[column]] = item.text()
                    # else:
                    #     row_data[headers[column]] = None  # 셀이 비어있는 경우 None으로 처리
                data.append(row_data)

            logger.info(f'data:{data}')
            for index, item in enumerate(data):
                resultObj[item['MSG_DT_VAL_ID']] = str(item['VALUE'])

            logger.info(f'{resultObj}')
            for key,val in enumerate(resultObj):
                logger.info(f'{val},:{resultObj[val]}')
                queryExecute(updateTbSkMsgVal(val, resultObj[val]))

        except:
            logger.error(f'saveDefaultVal error : {traceback.format_exc()}')