
from conf.logconfig import logger
import threading
import traceback
import schedule
import time
from src.protocols.BzActivator import BzActivator

class BzSchedule(threading.Thread):

    bzInfo = None
    interval = None # 시간 간격 (초단위)
    logger = None
    isRun = False
    times = time

    def __init__(self, bzInfo):
        # {'PKG_ID': 'CORE', 'SK_GROUP': 'TEST', 'BZ_TYPE': 'KEEP', 'USE_YN': 'Y', 'BZ_METHOD': 'TestController.test', 'SEC': None, 'BZ_DESC': None, 'CHANNEL':''}
        self.bzInfo = bzInfo
        self.interval = bzInfo['SEC']
        self.logger = bzInfo['LOGGER']
        self.logger.info(f'BzSchedule initData :{bzInfo}')
        super().__init__()

    def run(self):
        self.runSchedule()

    def runSchedule(self):
        try:
            self.isRun = True
            self.logger.info(f'BzSchedule start : SK_GROUP = {self.bzInfo["SK_GROUP"]} ')
            # self.schedule.every(self.interval).seconds.do(self.task)
            while self.isRun:
                self.times.sleep(self.interval)
                if self.isRun:
                    self.task()

        except Exception as e:
            self.isRun = False
            # self.logger.error(f'BzSchedule Exception :: {e}')
            self.logger.error(f'BzSchedule Exception :: {traceback.format_exc()}')

    def task(self):
        try:
            bz = BzActivator(self.bzInfo)
            bz.daemon = True
            bz.start()
        except Exception as e:
            self.logger.error(f'BzSchedule task exception : {e}')

    def stop(self):
        self.isRun = False

