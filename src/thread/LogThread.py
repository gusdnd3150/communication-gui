from ui.ui_log import Ui_Log
import logging
from PySide6.QtCore import QThread, Signal, Slot
import weakref
from collections import deque
import conf.skModule as moduleData

class LogThread(QThread):
    # 데이터를 수정하는 신호 정의
    updateLog = Signal(str)  # str
    msgQue = deque([])

    def __init__(self):
        super().__init__()

        text_edit_handler = QTextEditLogger(weakref.ref(self))
        text_edit_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(text_edit_handler)


    def setMsg(self, msg):
        try:
            self.msgQue.append(msg)
        except:
            self.msgQue.append('log setMsg error')

    def run(self): # 백그라운드 작업 실행
        try:
            while self.msgQue:  # 배열이 비어있지 않은 동안 반복
                self.updateLog.emit(self.msgQue.popleft())
        except:
            self.msgQue.clear()





class QTextEditLogger(logging.Handler):
    thread = None

    def __init__(self, thread):
        super().__init__()
        self.thread = thread

    def emit(self, record):
        if moduleData.mainLayout.log_chk_showlog.isChecked():
            msg = self.format(record)
            self.thread().setMsg(msg)
            self.thread().start()
            # self.mainUi.logThread.setMsg(msg)
            # self.mainUi.logThread.start()
        # self.text_edit.append(msg)