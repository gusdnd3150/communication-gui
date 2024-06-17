
from conf.logconfig import logger
import threading

class BzSchedule(threading.Thread):

    bzInfo = None
    skGroup = None

    def __init__(self, bzInfo):
        # {'PKG_ID': 'CORE', 'SK_GROUP': 'TEST', 'BZ_TYPE': 'KEEP', 'USE_YN': 'Y', 'BZ_METHOD': 'TestController.test', 'SEC': None, 'BZ_DESC': None, 'CHANNEL':''}
        self.bzInfo = bzInfo
        self.skGroup = bzInfo.get('SK_GROUP')
        super().__init__()

    def run(self):
        self.runSchedule()

    def runSchedule(self):
        try:
            logger.info(f'BzSchedule start : SK_GROUP = {self.bzInfo["SK_GROUP"]} ')


        except Exception as e:
            logger.info(f'BzSchedule Exception :: {e}')