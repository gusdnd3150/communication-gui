from conf.logconfig import logger
import threading
from src.protocols.BzActivator2 import BzActivator2
import traceback
import time
import schedule
from conf.logconfig import *
from concurrent.futures import ThreadPoolExecutor, as_completed

class Schedule(threading.Thread):

    bzInfo = None
    isRun = False
    schId = None
    schJob = None
    schjobTy = None
    times = time
    schedule = None
    executor = ThreadPoolExecutor(max_workers=10)

    # {'PKG_ID': 'CORE', 'SCH_ID': 'TEST', 'BZ_METHOD': 'TestController.sch', 'SCH_DESC': None, 'USE_YN': 'Y',
    #  'SCH_JOB': '2', 'SCH_JOB_TYPE': 'SEC'}
    def __init__(self, sch):

        self.bzInfo = sch
        self.schId = sch['SCH_ID']
        if sch.get('SCH_JOB') is not None:
            self.schJob = sch['SCH_JOB']

        if sch.get('SCH_JOB_TYPE') is not None:
            self.schjobTy = sch['SCH_JOB_TYPE']

        self.schedule = schedule

        super(Schedule, self).__init__()
        self._stop_event = threading.Event()

    def run(self):
        self.runSchedule()

    def stop(self):
        try:
            logger = logging.getLogger(self.schId)
            # 모든 핸들러 제거
            handlers = logger.handlers[:]
            for handler in handlers:
                handler.close()
                logger.removeHandler(handler)
            # 로거 제거
            logging.getLogger(self.schId).handlers = []

            self.schedule.clear()
            self.schedule = None
            self.isRun = False
        except Exception as e:
            logger.error(f'SCH_ID:{self.schId} Stop fail')
        finally:
            self._stop_event.set()
            # moduleData.mainInstance.deleteTableRow(self.skId, 'list_run_server')

    def __del__(self):
        logger.info('system schedules deleted')

    def runSchedule(self):
        try:
            sleep_time = 0
            if self.schjobTy == 'SEC':
                sleep_time = int(self.schJob)
            elif self.schjobTy == 'MIN':
                sleep_time = int(self.schJob) * 60
            elif self.schjobTy == 'HOUR':
                sleep_time = int(self.schJob) * 3600
            elif self.schjobTy == 'CRON':
                logger.info(f'cron')

            self.isRun = True
            self.schedule.every(sleep_time).seconds.do(self.task)
            while self.isRun:
                time.sleep(1)
                self.schedule.run_pending()

        except Exception as e:
            self.isRun = False
            if self.schedule is not None:
                self.schedule.clear()

            logger.error(f'system runSchedule Exception :: {traceback.format_exc()}')


    def task(self):
        try:
            if self.isRun:
                # start_time = time.time()
                futures = self.executor.submit(BzActivator2(self.bzInfo).run)
            # result = futures.result() #다른 스레드에 영향을 미침

            # 운영시 비권장 futures의 블락을 우회하기위해 스레드 선언
            # result_thread = threading.Thread(target=self.process_result, args=(futures, msg, start_time,))
            # result_thread.daemon = True
            # result_thread.start()
        except:
            logger.info(f'threadPoolExcutor exception :  {self.bzInfo["SK_GROUP"]}- {traceback.format_exc()}')

