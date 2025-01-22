from ui.ui_log import Ui_Log
import logging
from PySide6.QtCore import QThread, Signal, Slot

from collections import deque

class LogThread(QThread):
    # 데이터를 수정하는 신호 정의
    updateLog = Signal(str)  # str
    msgQue = deque([])

    def __init__(self, mainUi):
        super().__init__()
        text_edit_handler = QTextEditLogger(self, mainUi)
        text_edit_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(text_edit_handler)


    def setMsg(self, msg):
        self.msgQue.append(msg)

    def run(self): # 백그라운드 작업 실행
        while self.msgQue:  # 배열이 비어있지 않은 동안 반복
            self.updateLog.emit(self.msgQue.popleft())



class QTextEditLogger(logging.Handler):
    mainUi = None
    thread = None

    def __init__(self, thread, mainUi):
        super().__init__()
        # self.text_edit = text_edit
        self.mainUi = mainUi
        self.thread = thread

    def emit(self, record):
        if self.mainUi.ui.log_chk_showlog.isChecked():
            msg = self.format(record)
            self.thread.setMsg(msg)
            self.thread.start()
            # self.mainUi.logThread.setMsg(msg)
            # self.mainUi.logThread.start()
        # self.text_edit.append(msg)