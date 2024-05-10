
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QTabWidget, QPushButton, QCheckBox
import json

from src.component.settings.SaveSocketPopup import SaveSocketPopup
import sys
import os

program_path = sys.argv[0]
program_directory = os.path.dirname(program_path)

import traceback
from conf.logconfig import logger

import json

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class Settings():
    instance = None
    saveSkWindow = None
    sokcetList = []
    socketHd = []
    socketHdDt = []
    socketBody = []
    socketBodyDt = []
    socketVal = []
    sokcetBz = []
    sokcetIn = []
    sokcetInToOut = []
    sokcetOut = []
    sokcetSub = []
    sokcetSch = []

    def __init__(self):
        self.instance = QUiLoader().load(resource_path('views/settings.ui'), None)
        self.instance.setWindowTitle('설정')

        # 메시지 저장 팝업
        self.saveSkWindow = SaveSocketPopup(resource_path('views/settings-saveSocket.ui'))
        self.saveSkWindow.instance.setWindowTitle('추가')
        # self.saveSkWindow.instance.show()

        self.setEvent()
        self.loadData()

    def setEvent(self):
        self.instance.btn_addData.clicked.connect(self.addData)


    def addData(self):
        try:
            logger.info("addData")
            if self.saveSkWindow.instance.isVisible():
                self.saveSkWindow.instance.hide()
                self.saveSkWindow.clearForm()
            else:
                # 0: sk, 1: sk_in
                tapIndex =self.instance.tap_info.currentIndex()
                self.saveSkWindow.setForm(tapIndex,self.sokcetList[0].keys())
                self.saveSkWindow.instance.show()
        except:
            print('s')


    def loadJsonFile(self, fileNm):
        try:
            logger.info(program_directory+'/json/'+fileNm+'.json')
            with open(program_directory+'/json/'+fileNm+'.json', 'rt', encoding='UTF8') as f:
                data = json.load(f)
                return data
        except:
            traceback.print_exc()


    def loadData(self):
        self.sokcetList = self.loadJsonFile('TB_SK_PKG_SK')
        self.setTableData('list_sk')

        self.socketHd = self.loadJsonFile('TB_SK_MSG_HD')
        self.setTableData('list_hd')
        self.socketHdDt = self.loadJsonFile('TB_SK_MSG_HD_DT')

        self.socketBody = self.loadJsonFile('TB_SK_MSG_BODY')
        self.socketBodyDt = self.loadJsonFile('TB_SK_MSG_BODY_DT')
        self.socketVal = self.loadJsonFile('TB_SK_MSG_VAL')
        self.sokcetBz = self.loadJsonFile('TB_SK_PKG_SK_BZ')
        self.sokcetIn = self.loadJsonFile('TB_SK_PKG_SK_IN')
        self.sokcetInToOut = self.loadJsonFile('TB_SK_PKG_SK_IN_TO_OUT')
        self.sokcetOut = self.loadJsonFile('TB_SK_PKG_SK_OUT')
        self.sokcetSub = self.loadJsonFile('TB_SK_PKG_SK_SUB')
        self.sokcetSch = self.loadJsonFile('TB_SK_PKG_SCH')




    def save_clicked(self):
        # button = self.sender()
        button = self.instance.focusWidget()
        table = button.parentWidget().parentWidget() #버튼의 상위 위젯을 찾는다
        index = table.indexAt(button.pos())
        jsonData = {}
        if index.isValid():
            row = index.row()   # column = index.column()
            tableNm = table.objectName()
            if(tableNm == 'list_sk'):
                # self.sokcetList[0].keys()
                idx = 0
                for key in self.sokcetList[0].keys():
                    jsonData[key] = table.item(row,idx).text()
                    idx = idx+1
                self.sokcetList[row] = jsonData

        logger.info(self.sokcetList[row])

    def delete_clicked(self):
        # button = self.sender()
        button = self.instance.focusWidget()
        table = button.parentWidget().parentWidget() #버튼의 상위 위젯을 찾는다
        index = table.indexAt(button.pos())
        jsonData = {}
        if index.isValid():
            row = index.row()   # column = index.column()
            tableNm = table.objectName()
            if(tableNm == 'list_sk'):
                # self.sokcetList[0].keys()
                idx = 0
                for key in self.sokcetList[0].keys():
                    jsonData[key] = table.item(row,idx).text()
                    idx = idx+1
                self.sokcetList[row] = jsonData

        logger.info(self.sokcetList[row])

    def setTableData(self, target):
        try:
            if(target == 'list_sk'):
                # 데이터의 행과 열 수를 얻습니다.
                rows = len(self.sokcetList)
                cols = len(self.sokcetList[0]) if rows > 0 else 0
                self.instance.list_sk.setRowCount(rows)  # Table의 행을 설정, list의 길이
                self.instance.list_sk.setColumnCount(cols+1)
                self.instance.list_sk.setHorizontalHeaderLabels(self.sokcetList[0].keys())
                # 데이터를 테이블에 삽입
                for i, row in enumerate(self.sokcetList):
                    last = 0
                    for j, item in enumerate(row):
                        last = last+1
                        self.instance.list_sk.setItem(i, j, QTableWidgetItem(row[item]))
                    button = QPushButton('삭제')
                    button.clicked.connect(self.save_clicked)
                    self.instance.list_sk.setCellWidget(i, last, button)

            elif(target == 'list_hd'):
                # 데이터의 행과 열 수를 얻습니다.
                rows = len(self.socketHd)
                cols = len(self.socketHd[0]) if rows > 0 else 0
                self.instance.list_hd.setRowCount(rows)  # Table의 행을 설정, list의 길이
                self.instance.list_hd.setColumnCount(cols+1)
                self.instance.list_hd.setHorizontalHeaderLabels(self.socketHd[0].keys())
                # 데이터를 테이블에 삽입
                for i, row in enumerate(self.socketHd):
                    for j, item in enumerate(row):
                        self.instance.list_hd.setItem(i, j, QTableWidgetItem(row[item]))
        except:
            traceback.print_stack()


