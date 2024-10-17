
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QTableWidgetItem, QMainWindow, QHeaderView
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget
from PySide6.QtCore import QSize

import sys
import os
import src.protocols.SendHandler as SendHandler
program_path = sys.argv[0]
program_directory = os.path.dirname(program_path)
import traceback
from conf.skModule import *
from conf.sql.SystemQueryString import *
from ui.ui_log import Ui_Log
import logging
from PySide6.QtCore import QThread, Signal, Slot



class LogThread(QThread):
    # 데이터를 수정하는 신호 정의
    updateLog = Signal(str)  # row, column, data
    msgQue = []
    def __init__(self):
        super().__init__()

    def setMsg(self, msg):
        self.msgQue.append(msg)

    def run(self): # 백그라운드 작업 실행
        while self.msgQue:  # 배열이 비어있지 않은 동안 반복
            self.updateLog.emit(self.msgQue.pop())



class Log(QMainWindow):

    saveSkWindow = None
    initData = None
    skRow = None
    contFlag = 'upd'
    msgId = None
    isChk = False
    logThread = None

    def __init__(self, initData):
        super(Log, self).__init__()
        self.initData = initData
        self.ui = Ui_Log()
        self.ui.setupUi(self)
        self.setWindowTitle('logging')
        self.setEvent()



    def setEvent(self):
        # self.ui.log_text_log.setMaximumSize(QSize(10))

        self.ui.log_btn_clear.clicked.connect(self.clickClear)
        self.ui.log_btn_openFoler.clicked.connect(self.openFolder)
        self.ui.log_chk_showlog.stateChanged.connect(self.setChk)
        self.ui.log_text_log.setReadOnly(True)  # 편집 불가능하도록 설정
        self.logThread = LogThread()
        self.logThread.updateLog.connect(self.showLog)  # 신호 연결

        text_edit_handler = QTextEditLogger(self.ui.log_text_log, self)
        text_edit_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(text_edit_handler)


    def openFolder(self):
        try:
            # 열고 싶은 경로
            path = r"../logs/"
            current_path = os.getcwd()
            # logger.info(f'path : {current_path}')
            # 경로 열기
            os.startfile(f'{current_path}/logs')
        except:
            traceback.format_exc()


    def setChk(self):
        self.isChk = self.ui.log_chk_showlog.isChecked()

    def clickClear(self):
        self.ui.log_text_log.clear()


    @Slot(str)
    def showLog(self, msg):
        try:
            # logger.info(f'showLog : {msg}')
            self.ui.log_text_log.append(msg)
        except:
            logger.error(f'showLog error : {traceback.format_exc()}')



class QTextEditLogger(logging.Handler):
    log = None

    def __init__(self, text_edit, log):
        super().__init__()
        # self.text_edit = text_edit
        self.log = log

    def emit(self, record):
        if self.log.isChk:
            msg = self.format(record)
            self.log.logThread.setMsg(msg)
            self.log.logThread.start()
        # self.text_edit.append(msg)

