
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QTabWidget, QPushButton, QCheckBox, QMainWindow
import json
from src.component.settings.SaveSocketPopup import SaveSocketPopup
import sys
import os

program_path = sys.argv[0]
program_directory = os.path.dirname(program_path)

import traceback
from conf.logconfig import logger
from conf.InitData_n import *
from conf.QueryString import *
import json

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class Settings(QMainWindow):

    instance = None
    saveSkWindow = None
    initData = None

    def __init__(self, initData):
        self.initData = initData
        self.ui = QUiLoader().load(resource_path('views/settings.ui'), None)
        super().__init__()
        self.setCentralWidget(self.ui)
        self.setWindowTitle('설정')

        # 메시지 저장 팝업
        self.saveSkWindow = SaveSocketPopup(resource_path('views/settings-saveSocket.ui'))
        self.saveSkWindow.instance.setWindowTitle('추가')
        # self.saveSkWindow.instance.show()

        self.setEvent()
        self.createSkGrid() # 소켓 그리드

    def setEvent(self):
        self.ui.btn_addSk.clicked.connect(self.addSk)
        self.ui.btn_delSk.clicked.connect(self.delSk)
        self.ui.btn_saveSk.clicked.connect(self.delSk)

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
            # logger.info(f'row: {row}')
            # item = self.ui.list_sk.item(row, column)
            # if item:
            #     print(f"Item text: {item.text()}")
            row_data = {}
            for column in range(self.ui.list_sk.columnCount()):
                header_item = self.ui.list_sk.horizontalHeaderItem(column)
                item = self.ui.list_sk.item(row, column)
                row_data[header_item.text()] = item.text() if item else ""

            self.ui.sk_PKG_ID.setText(row_data['PKG_ID'])
            self.ui.sk_SK_ID.setText(row_data['SK_ID'])
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
        self.addControll('list_sk')

    def delSk(self):
        self.addControll('list_sk')

    def saveSk(self):
        self.addControll('list_sk')
