
import traceback
from conf.logconfig import logger
import threading
class SocketServer(threading.Thread):

    initData = {}
    skId = ''
    def __init__(self, data):
        self.initData = data
        self.skId = data['SK_ID']
        self.name = data['SK_ID']+'-thread'
        threading.Thread.__init__(self)

    def run(self):
        try:
            logger.info('TCP SERVER Start : '+ self.skId +' ::'+ threading.currentThread().getName())


        except:
            traceback.print_stack()
