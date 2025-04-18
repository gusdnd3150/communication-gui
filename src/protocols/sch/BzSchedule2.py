
from conf.logconfig import logger
import threading
import traceback
import time
from src.protocols.BzActivator2 import BzActivator2
import schedule
from concurrent.futures import ThreadPoolExecutor

class BzSchedule2(threading.Thread):

    bzInfo = None
    interval = None # 시간 간격 (초단위)
    logger = None
    isRun = False
    times = time
    executor = ThreadPoolExecutor(max_workers=10)
    schedule = None

    def __init__(self, bzInfo):
        # {'PKG_ID': 'CORE', 'SK_GROUP': 'TEST', 'BZ_TYPE': 'KEEP', 'USE_YN': 'Y', 'BZ_METHOD': 'TestController.test', 'SEC': None, 'BZ_DESC': None, 'CHANNEL':''}
        self.bzInfo = bzInfo
        self.interval = bzInfo['SEC']
        self.logger = bzInfo['LOGGER']
        self.logger.info(f'BzSchedule initData :{bzInfo}')

        self.schedule = schedule
        super(BzSchedule2, self).__init__()
        self._stop_event = threading.Event()

    def run(self):
        self.runSchedule()

    def __del__(self):
        logger.info(f'Schedules Thread SK_GROUP = {self.bzInfo["SK_GROUP"]} is deleted')

    def runSchedule(self):
        try:
            self.isRun = True
            self.logger.info(f'BzSchedule start : SK_GROUP = {self.bzInfo["SK_GROUP"]} ')
            self.schedule.every(self.interval).seconds.do(self.task)
            while self.isRun:
                time.sleep(1)
                if self.schedule is not None:
                    self.schedule.run_pending()

        except Exception as e:
            self.isRun = False
            if self.schedule is not None:
                self.schedule.clear()

            self.logger.error(f'BzSchedule Exception :: {traceback.format_exc()}')

    def task(self):
        try:
            if self.isRun:
                futures = self.executor.submit(BzActivator2(self.bzInfo).run)
        except:
            self.logger.info(f'threadPoolExcutor exception :  {self.bzInfo["SK_GROUP"]}- {traceback.format_exc()}')



    def stop(self):
        try:
            self._stop_event.set()
            self.schedule.clear()
            self.schedule = None
            self.isRun = False
            # self.executor.shutdown()
        except:
            self.logger.error(f'stop schedulse exception : {traceback.format_exc()}')



