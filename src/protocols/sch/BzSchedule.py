
from conf.logconfig import logger
import threading

class BzSchedule(threading.Thread):
    initData = None

    def __init__(self, initData):
        self.initData = initData
        # {'PKG_ID': 'CORE', 'SK_GROUP': 'TEST', 'BZ_TYPE': 'KEEP', 'USE_YN': 'Y', 'BZ_METHOD': 'TestController.test', 'SEC': None, 'BZ_DESC': None, 'CHANNEL':''}
        super().__init__()
        self.name = 'Thread Schedule'

    def run(self):
        self.runSchedule()


    def runSchedule(self):
        try:
            logger.info(f'BzSchedule start : SK_GROUP = {self.initData["SK_GROUP"]} ')


        except Exception as e:
            logger.info(f'BzSchedule Exception :: {e}')