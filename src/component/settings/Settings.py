
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

    def setEvent(self):
        self.ui.btn_addSk.clicked.connect(self.addSk)
        self.ui.btn_delSk.clicked.connect(self.delSk)



    def addControll(self, target):
        logger.info('addControll :'+ target)
        try:

            if(target == 'list_sk'): # sk add 버튼
                logger.info('add row : list_sk')
                addIndex = self.instance.list_sk.rowCount()

                # self.instance.list_sk.setItem(QTableWidgetItem())
                # self.instance.list_sk.insertRow(addIndex)

                for index, item in enumerate(self.initData.sokcetList[0]):
                    logger.info(str(addIndex))
                    self.instance.list_sk.setItem(addIndex, index, QTableWidgetItem(''))

            # logger.info("addData")
            # if self.saveSkWindow.instance.isVisible():
            #     self.saveSkWindow.instance.hide()
            #     self.saveSkWindow.clearForm()
            # else:
            #     # 0: sk, 1: sk_in
            #     tapIndex = self.instance.tap_info.currentIndex()
            #     self.saveSkWindow.setForm(tapIndex, self.sokcetList[0].keys())
            #     self.saveSkWindow.instance.show()
        except:
            traceback.print_exception()


    def addSk(self):
        self.addControll('list_sk')

    def delSk(self):
        self.addControll('list_sk')


    def loadData(self):
        self.setTableData('list_sk')
        self.setTableData('list_hd')
        self.setTableData('list_hd_dt')
        self.setTableData('list_in')
        self.setTableData('list_msg')
        self.setTableData('list_msg_dt')
        self.setTableData('list_dt_val')
        self.setTableData('list_sch')





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
                list = self.initData.sokcetList
                rows = len(list)
                cols = len(list[0]) if rows > 0 else 0
                self.instance.list_sk.setRowCount(rows)  # Table의 행을 설정, list의 길이
                self.instance.list_sk.setColumnCount(cols)
                self.instance.list_sk.setHorizontalHeaderLabels(list[0].keys())
                # 데이터를 테이블에 삽입
                for i, row in enumerate(list):
                    last = 0
                    for j, item in enumerate(row):
                        last = last+1
                        self.instance.list_sk.setItem(i, j, QTableWidgetItem(row[item]))
                    # button = QPushButton('삭제')
                    # button.clicked.connect(self.save_clicked)
                    # self.instance.list_sk.setCellWidget(i, last, button)

            elif(target == 'list_hd'):
                # 데이터의 행과 열 수를 얻습니다.
                list = self.initData.socketHd
                rows = len(list)
                cols = len(list[0]) if rows > 0 else 0
                self.instance.list_hd.setRowCount(rows)  # Table의 행을 설정, list의 길이
                self.instance.list_hd.setColumnCount(cols)
                self.instance.list_hd.setHorizontalHeaderLabels(list[0].keys())
                # 데이터를 테이블에 삽입
                for i, row in enumerate(list):
                    for j, item in enumerate(row):
                        self.instance.list_hd.setItem(i, j, QTableWidgetItem(row[item]))
            elif (target == 'list_hd_dt'):
                # 데이터의 행과 열 수를 얻습니다.
                list = self.initData.socketHdDt
                rows = len(list)
                cols = len(list[0]) if rows > 0 else 0
                self.instance.list_hd_dt.setRowCount(rows)  # Table의 행을 설정, list의 길이
                self.instance.list_hd_dt.setColumnCount(cols)
                self.instance.list_hd_dt.setHorizontalHeaderLabels(list[0].keys())
                # 데이터를 테이블에 삽입
                for i, row in enumerate(list):
                    for j, item in enumerate(row):
                        self.instance.list_hd_dt.setItem(i, j, QTableWidgetItem(row[item]))
            elif (target == 'list_in'):
                # 데이터의 행과 열 수를 얻습니다.
                list = self.initData.sokcetIn
                rows = len(list)
                cols = len(list[0]) if rows > 0 else 0
                self.instance.list_in.setRowCount(rows)  # Table의 행을 설정, list의 길이
                self.instance.list_in.setColumnCount(cols)
                self.instance.list_in.setHorizontalHeaderLabels(list[0].keys())
                # 데이터를 테이블에 삽입
                for i, row in enumerate(list):
                    for j, item in enumerate(row):
                        self.instance.list_in.setItem(i, j, QTableWidgetItem(row[item]))


            elif (target == 'list_msg'):
                # 데이터의 행과 열 수를 얻습니다.
                list = self.initData.socketBody
                rows = len(list)
                cols = len(list[0]) if rows > 0 else 0
                self.instance.list_msg.setRowCount(rows)  # Table의 행을 설정, list의 길이
                self.instance.list_msg.setColumnCount(cols)
                self.instance.list_msg.setHorizontalHeaderLabels(list[0].keys())
                # 데이터를 테이블에 삽입
                for i, row in enumerate(list):
                    for j, item in enumerate(row):
                        self.instance.list_msg.setItem(i, j, QTableWidgetItem(row[item]))

            elif (target == 'list_msg_dt'):
                # 데이터의 행과 열 수를 얻습니다.
                list = self.initData.socketBodyDt
                rows = len(list)
                cols = len(list[0]) if rows > 0 else 0
                self.instance.list_msg_dt.setRowCount(rows)  # Table의 행을 설정, list의 길이
                self.instance.list_msg_dt.setColumnCount(cols)
                self.instance.list_msg_dt.setHorizontalHeaderLabels(list[0].keys())
                # 데이터를 테이블에 삽입
                for i, row in enumerate(list):
                    for j, item in enumerate(row):
                        self.instance.list_msg_dt.setItem(i, j, QTableWidgetItem(row[item]))

            elif (target == 'list_dt_val'):
                # 데이터의 행과 열 수를 얻습니다.
                list = self.initData.socketVal
                rows = len(list)
                cols = len(list[0]) if rows > 0 else 0
                self.instance.list_dt_val.setRowCount(rows)  # Table의 행을 설정, list의 길이
                self.instance.list_dt_val.setColumnCount(cols)
                self.instance.list_dt_val.setHorizontalHeaderLabels(list[0].keys())
                # 데이터를 테이블에 삽입
                for i, row in enumerate(list):
                    for j, item in enumerate(row):
                        self.instance.list_dt_val.setItem(i, j, QTableWidgetItem(row[item]))

            elif (target == 'list_sch'):
                # 데이터의 행과 열 수를 얻습니다.
                list = self.initData.sokcetSch
                rows = len(list)
                cols = len(list[0]) if rows > 0 else 0
                self.instance.list_sch.setRowCount(rows)  # Table의 행을 설정, list의 길이
                self.instance.list_sch.setColumnCount(cols)
                self.instance.list_sch.setHorizontalHeaderLabels(list[0].keys())
                # 데이터를 테이블에 삽입
                for i, row in enumerate(list):
                    for j, item in enumerate(row):
                        self.instance.list_sch.setItem(i, j, QTableWidgetItem(row[item]))

        except:
            traceback.print_stack()


