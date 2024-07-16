
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QTableWidgetItem, QMainWindow, QHeaderView
from src.component.settings.SaveSocketPopup import SaveSocketPopup
import sys
import os

program_path = sys.argv[0]
program_directory = os.path.dirname(program_path)

import traceback
from conf.skModule import *
from conf.sql.SystemQueryString import *


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
resource_path('settings.ui')

class Handler(QMainWindow):

    saveSkWindow = None
    initData = None
    skRow = None
    contFlag = 'upd'

    def __init__(self, initData):
        self.initData = initData
        # path = resource_path('views\settings.ui')
        path = resource_path('handler.ui')
        logger.info(f'path : {path}')
        self.ui = QUiLoader().load(path, None)
        super().__init__()
        self.setCentralWidget(self.ui)
        self.setWindowTitle('핸들러')

        self.setEvent()
        self.createSkGrid() # 소켓 그리드


    def setEvent(self):

        # 소켓 탭 이벤트 설정
        self.ui.btn_addSk.clicked.connect(self.addSk)
        self.ui.btn_delSk.clicked.connect(self.delSk)
        self.ui.btn_saveSk.clicked.connect(self.saveSk)

        for item in useYnCombo:
            self.ui.sk_USE_YN.addItem(item)
            self.ui.sk_SK_LOG.addItem(item)
            self.ui.in_USE_YN.addItem(item)
            self.ui.bz_USE_YN.addItem(item)
            self.ui.sch_USE_YN.addItem(item)


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

