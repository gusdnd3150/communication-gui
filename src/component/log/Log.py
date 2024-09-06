
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QTableWidgetItem, QMainWindow, QHeaderView
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget
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

    def __init__(self, initData):
        super(Log, self).__init__()
        self.initData = initData
        self.ui = Ui_Log()
        self.ui.setupUi(self)
        self.setWindowTitle('logging')

        self.setEvent()
        # self.createMsgGrid(None,None)


    def setEvent(self):
        self.ui.log_text_log.setReadOnly(True)  # 편집 불가능하도록 설정
        # self.ui.log_text_log.setMaximumSize(1000)  # 최대 1000줄로 제한
        text_edit_handler = QTextEditLogger(self.ui.log_text_log)
        text_edit_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(text_edit_handler)
        # # FileHandler 설정
        # file_handler = logging.FileHandler("application.log")  # 로그 파일 설정
        # file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        # logging.getLogger().addHandler(file_handler)
        # # 로그 레벨 설정
        # logging.getLogger().setLevel(logging.DEBUG)



class QTextEditLogger(logging.Handler):
    def __init__(self, text_edit):
        super().__init__()
        self.text_edit = text_edit

    def emit(self, record):
        msg = self.format(record)
        self.text_edit.append(msg)
