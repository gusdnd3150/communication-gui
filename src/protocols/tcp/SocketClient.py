

from conf.logconfig import logger
import threading
import time
import traceback

class SocketClient(threading.Thread):

    initData = {}
    skId = ''
    
    def __init__(self, data):
        self.initData = data
        self.skId = data['SK_ID']
        self.name = data['SK_ID']+'-thread'  # 스레드 이름 설정
        threading.Thread.__init__(self)


    def run(self):
        try:
            logger.info('TCP Client Start : ' + self.skId +' ::'+ threading.currentThread().getName())

        except:
            logger.info('sss')
