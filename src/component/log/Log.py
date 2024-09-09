
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

class Log(QMainWindow):

    saveSkWindow = None
    initData = None
    skRow = None
    contFlag = 'upd'
    msgId = None
    isChk = False

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
        self.ui.log_chk_showlog.stateChanged.connect(self.setChk)
        self.ui.log_text_log.setReadOnly(True)  # 편집 불가능하도록 설정
        text_edit_handler = QTextEditLogger(self.ui.log_text_log, self)
        text_edit_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(text_edit_handler)

    def setChk(self):
        self.isChk = self.ui.log_chk_showlog.isChecked()

    def clickClear(self):
        logger.info(f'testsets')
        self.ui.log_text_log.clear()

class QTextEditLogger(logging.Handler):
    log = None

    def __init__(self, text_edit, log):
        super().__init__()
        self.text_edit = text_edit
        self.log = log

    def emit(self, record):
        msg = self.format(record)
        self.text_edit.append(msg)

