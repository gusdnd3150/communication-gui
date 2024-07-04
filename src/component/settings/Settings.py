
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QTableWidgetItem, QMainWindow, QHeaderView
from src.component.settings.SaveSocketPopup import SaveSocketPopup
import sys
import os

program_path = sys.argv[0]
program_directory = os.path.dirname(program_path)

import traceback
from conf.InitData import *
from conf.sql.SystemQueryString import *


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
resource_path('settings.ui')

class Settings(QMainWindow):

    instance = None
    saveSkWindow = None
    initData = None
    skRow = None
    contFlag = 'upd'

    def __init__(self, initData):
        self.initData = initData
        # path = resource_path('views\settings.ui')
        path = resource_path('settings.ui')
        logger.info(f'path : {path}')
        self.ui = QUiLoader().load(path, None)

        super().__init__()
        self.setCentralWidget(self.ui)
        self.setWindowTitle('설정')

        # 메시지 저장 팝업

        # self.saveSkWindow = SaveSocketPopup('./src/component/settings/views/settings-saveSocket.ui')
        self.saveSkWindow = SaveSocketPopup()
        self.saveSkWindow.instance.setWindowTitle('추가')
        # self.saveSkWindow.instance.show()

        self.setEvent()
        self.createSkGrid() # 소켓 그리드
        self.createMsgGrid(None,None)

    def setEvent(self):
        self.ui.btn_addSk.clicked.connect(self.addSk)
        self.ui.btn_delSk.clicked.connect(self.delSk)
        self.ui.btn_saveSk.clicked.connect(self.saveSk)


        self.ui.msg_search.clicked.connect(self.searchMsg)

        for item in useYnCombo:
            self.ui.sk_USE_YN.addItem(item)
            self.ui.sk_SK_LOG.addItem(item)

        for item in skTypeCombo:
            self.ui.sk_SK_TYPE.addItem(item)

        for item in skConnCombo:
            self.ui.sk_SK_CONN_TYPE.addItem(item)

        for item in skClientCombo:
            self.ui.sk_SK_CLIENT_TYPE.addItem(item)
        for item in hdCombo:
            self.ui.sk_HD_ID.addItem(item)


    def createSkGrid(self):
        try:
            headers = ['PKG_ID', 'SK_ID','USE_YN', 'SK_GROUP', 'SK_TYPE', 'SK_CONN_TYPE', 'SK_CLIENT_TYPE', 'HD_ID', 'SK_IP',
                       'SK_PORT', 'SK_DELIMIT_TYPE', 'SK_LOG', 'SK_DESC']

            self.ui.list_sk.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            self.ui.list_sk.verticalHeader().setVisible(False)

            self.ui.list_sk.setRowCount(0)  # Table의 행을 설정, list의 길이
            self.ui.list_sk.setColumnCount(13)
            self.ui.list_sk.setHorizontalHeaderLabels(headers)
            skList = selectQuery(selectSocketList(None, None, None))
            for i, skItem in enumerate(skList):
                row_count = self.ui.list_sk.rowCount()
                self.ui.list_sk.insertRow(row_count)
                for j, hd in enumerate(headers):
                    if skItem.get(hd) is not None:
                        self.ui.list_sk.setItem(row_count, j, QTableWidgetItem(str(skItem[hd])))
            self.ui.list_sk.cellClicked.connect(self.selectRow)

        except Exception as e:
            logger.info(f'createGrid exception : {traceback.format_exc()}')


    def selectRow(self,row, column):
        try:
            self.contFlag = 'upd'
            # logger.info(f'row: {row}')
            # item = self.ui.list_sk.item(row, column)
            # if item:
            #     print(f"Item text: {item.text()}")
            row_data = {}
            for column in range(self.ui.list_sk.columnCount()):
                header_item = self.ui.list_sk.horizontalHeaderItem(column)
                item = self.ui.list_sk.item(row, column)
                row_data[header_item.text()] = item.text() if item else ""
            self.skRow = row
            self.ui.sk_PKG_ID.setText(row_data['PKG_ID'])
            self.ui.sk_PKG_ID.setDisabled(True)
            self.ui.sk_SK_ID.setText(row_data['SK_ID'])
            self.ui.sk_SK_ID.setDisabled(True)
            self.ui.sk_SK_GROUP.setText(row_data['SK_GROUP'])
            self.ui.sk_SK_IP.setText(row_data['SK_IP'])
            self.ui.sk_SK_PORT.setText(row_data['SK_PORT'])
            self.ui.sk_SK_DELIMIT_TYPE.setText(row_data['SK_DELIMIT_TYPE'])
            self.ui.sk_SK_DESC.setText(row_data['SK_DESC'])

            self.ui.sk_USE_YN.setCurrentText(row_data['USE_YN'])
            self.ui.sk_SK_CONN_TYPE.setCurrentText(row_data['SK_CONN_TYPE'])
            self.ui.sk_SK_CLIENT_TYPE.setCurrentText(row_data['SK_CLIENT_TYPE'])
            self.ui.sk_HD_ID.setCurrentText(row_data['HD_ID'])
            self.ui.sk_SK_LOG.setCurrentText(row_data['SK_LOG'])


        except Exception as e :
            logger.error(f'selectRow exception : {traceback.format_exc()} ')

    def addSk(self):
        self.contFlag = 'ins'
        self.skRow = None
        self.ui.sk_PKG_ID.setText('')
        self.ui.sk_PKG_ID.setDisabled(False)
        self.ui.sk_SK_ID.setText('')
        self.ui.sk_SK_ID.setDisabled(False)
        self.ui.sk_SK_GROUP.setText('')
        self.ui.sk_SK_IP.setText('')
        self.ui.sk_SK_PORT.setText('')
        self.ui.sk_SK_DELIMIT_TYPE.setText('')
        self.ui.sk_SK_DESC.setText('')


    def delSk(self):
        logger.info(f'delete row : {self.skRow}')
        queryExecute(delSk(self.ui.sk_PKG_ID.text(), self.ui.sk_SK_ID.text()))
        self.createSkGrid()

    def saveSk(self):
        row_data = {
            'SK_GROUP': self.ui.sk_SK_GROUP.text()
            , 'USE_YN': self.ui.sk_USE_YN.currentText()
            , 'SK_TYPE': self.ui.sk_SK_TYPE.currentText()
            , 'SK_CONN_TYPE': self.ui.sk_SK_CONN_TYPE.currentText()
            , 'SK_CLIENT_TYPE': self.ui.sk_SK_CLIENT_TYPE.currentText()
            , 'HD_ID': self.ui.sk_HD_ID.currentText()
            , 'SK_IP': self.ui.sk_SK_IP.text()
            , 'SK_PORT': self.ui.sk_SK_PORT.text()
            , 'SK_LOG': self.ui.sk_SK_LOG.currentText()
            , 'SK_DELIMIT_TYPE': self.ui.sk_SK_DELIMIT_TYPE.text()
            , 'SK_DESC': self.ui.sk_SK_DESC.toPlainText()
        }
        if self.contFlag == 'ins':
            row_data['SK_ID'] = self.ui.sk_SK_ID.text()
            row_data['PKG_ID'] = self.ui.sk_PKG_ID.text()
            queryExecute(insertSK(row_data))
        else :
            queryExecute(saveSk(self.ui.sk_PKG_ID.text(), self.ui.sk_SK_ID.text(), row_data))
        self.createSkGrid()
        logger.info(f'{row_data}')

#################################################################### 메시지

    def searchMsg(self):
        try:

            logger.info(f'sss : {self.ui.msg_MSG_MID_iq.text()}')
            logger.info(f'sss : {self.ui.msg_MSG_ID_iq.text()}')
            self.createMsgGrid(self.ui.msg_MSG_ID_iq.text(),self.ui.msg_MSG_MID_iq.text())
            self.createMsgDtGrid(self.ui.msg_MSG_ID_iq.text())
        except Exception as e:
            logger.error(f'searchMsg exception : {traceback.format_exc()}')
    def createMsgGrid(self, msg, mid):
        try:
            logger.info('test')
            headers = ['MSG_ID','MSG_KEY_TYPE','MSG_KEY_VAL','MSG_DESC' ]
            self.ui.msg_list.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            self.ui.msg_list.setRowCount(0)  # Table의 행을 설정, list의 길이
            self.ui.msg_list.setColumnCount(4)
            self.ui.msg_list.setHorizontalHeaderLabels(headers)
            skList = selectQuery(selectSocketMSgList(msg, mid))
            for i, skItem in enumerate(skList):
                row_count = self.ui.msg_list.rowCount()
                self.ui.msg_list.insertRow(row_count)
                for j, hd in enumerate(headers):
                    if skItem.get(hd) is not None:
                        self.ui.msg_list.setItem(row_count, j, QTableWidgetItem(str(skItem[hd])))
            self.ui.msg_list.cellClicked.connect(self.selectMsgRow)
        except Exception as e:
            logger.error(f'createMsgGrid exception : {traceback.format_exc()}')

    def selectMsgRow(self,row, column):
        try:
            # logger.info(f'row: {row}')
            # item = self.ui.list_sk.item(row, column)
            # if item:
            #     print(f"Item text: {item.text()}")
            row_data = {}
            for column in range(self.ui.msg_list.columnCount()):
                header_item = self.ui.msg_list.horizontalHeaderItem(column)
                item = self.ui.msg_list.item(row, column)
                row_data[header_item.text()] = item.text() if item else ""

            # self.ui.sk_PKG_ID.setText(row_data['PKG_ID'])
            self.createMsgDtGrid(row_data['MSG_ID'])

        except Exception as e :
            logger.error(f'selectMsgRow exception : {traceback.format_exc()} ')

    def createMsgDtGrid(self, msg):
        try:
            if msg is None or msg == '':
                return

            headers = ['MSG_DT_ORD','MSG_DT_VAL_ID','MSG_DT_DESC','VAL_TYPE','VAL_LEN' ]
            self.ui.msg_dt_list.setRowCount(0)  # Table의 행을 설정, list의 길이
            self.ui.msg_dt_list.setColumnCount(5)
            self.ui.msg_dt_list.setHorizontalHeaderLabels(headers)
            skList = selectQuery(selectSocketMSgDtList(msg))
            for i, skItem in enumerate(skList):
                row_count = self.ui.msg_dt_list.rowCount()
                self.ui.msg_dt_list.insertRow(row_count)
                for j, hd in enumerate(headers):
                    if skItem.get(hd) is not None:
                        self.ui.msg_dt_list.setItem(row_count, j, QTableWidgetItem(str(skItem[hd])))
            # self.ui.msg_dt_list.cellClicked.connect(self.selectMsgRow)
        except Exception as e:
            logger.error(f'createMsgGrid exception : {traceback.format_exc()}')