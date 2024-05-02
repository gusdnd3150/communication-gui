
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
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
        print()


    def loadJsonFile(self, fileNm):
        try:
            with open(program_directory+'/json/'+fileNm+'.json') as f:
                data = json.load(f)
                return data
        except:
            traceback.print_exc()


    def loadData(self):
        self.sokcetList = self.loadJsonFile('TB_SK_PKG_SK')
        logger.info(self.sokcetList)
        # 데이터의 행과 열 수를 얻습니다.
        rows = len(self.sokcetList)
        cols = len(self.sokcetList[0]) if rows > 0 else 0

        self.instance.list_sk.setRowCount(rows)  # Table의 행을 설정, list의 길이
        self.instance.list_sk.setColumnCount(cols)

        # 데이터를 테이블에 삽입
        for i, row in enumerate(self.sokcetList):
            logger.info(row)
            for j, item in enumerate(row):
                logger.info(item)
                self.instance.list_sk.setItem(i, j, QTableWidgetItem(row[item]))

