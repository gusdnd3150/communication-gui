
from conf.logconfig import logger
import threading
import traceback
import time
from src.protocols.BzActivator2 import BzActivator2
import schedule
from concurrent.futures import ThreadPoolExecutor, as_completed

class BzSchedule2(threading.Thread):

    bzInfo = None
    interval = None # 시간 간격 (초단위)
    logger = None
    isRun = False
    times = time
    executor = ThreadPoolExecutor(max_workers=10)

    def __init__(self, bzInfo):
        # {'PKG_ID': 'CORE', 'SK_GROUP': 'TEST', 'BZ_TYPE': 'KEEP', 'USE_YN': 'Y', 'BZ_METHOD': 'TestController.test', 'SEC': None, 'BZ_DESC': None, 'CHANNEL':''}
        self.bzInfo = bzInfo
        self.interval = bzInfo['SEC']
        self.logger = bzInfo['LOGGER']
        self.logger.info(f'BzSchedule initData :{bzInfo}')

        super(BzSchedule2, self).__init__()
        self._stop_event = threading.Event()

    def run(self):
        self.runSchedule()

    def runSchedule(self):
        try:
            self.isRun = True
            self.logger.info(f'BzSchedule start : SK_GROUP = {self.bzInfo["SK_GROUP"]} ')
            schedule.every(self.interval).seconds.do(self.task)
            while self.isRun:
                schedule.run_pending()
                time.sleep(1)
        except Exception as e:
            self.isRun = False
            schedule.clear()
            self.logger.error(f'BzSchedule Exception :: {traceback.format_exc()}')

    def task(self):
        try:
            start_time = time.time()
            futures = self.executor.submit(BzActivator2(self.bzInfo).run)
            # result = futures.result() #다른 스레드에 영향을 미침

            # 운영시 비권장 futures의 블락을 우회하기위해 스레드 선언
            # result_thread = threading.Thread(target=self.process_result, args=(futures, msg, start_time,))
            # result_thread.daemon = True
            # result_thread.start()
        except:
            self.logger.info(f'threadPoolExcutor exception : SK_ID:{self.skId} - {traceback.format_exc()}')



    def stop(self):
        self.isRun = False
        self._stop_event.set()
        self.executor.shutdown()


