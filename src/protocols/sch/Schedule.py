from conf.logconfig import logger
import threading
from src.protocols.BzActivator import BzActivator
import time
from datetime import datetime
from crontab import CronTab
import schedule
from conf.logconfig import *

class Schedule(threading.Thread):

    bzInfo = None
    isRun = False
    schId = None
    schJob = None
    schjobTy = None
    times = time
    logger = None

    # {'PKG_ID': 'CORE', 'SCH_ID': 'TEST', 'BZ_METHOD': 'TestController.sch', 'SCH_DESC': None, 'USE_YN': 'Y',
    #  'SCH_JOB': '2', 'SCH_JOB_TYPE': 'SEC'}
    def __init__(self, sch):
        logger.info(f'init sch :{sch}')
        self.bzInfo = sch
        if sch.get('SCH_JOB') is not None:
            self.schJob = sch['SCH_JOB']

        if sch.get('SCH_JOB_TYPE') is not None:
            self.schjobTy = sch['SCH_JOB_TYPE']

        self.logger = setup_sk_logger(sch['SCH_ID'])
        self.bzInfo['LOGGER'] = self.logger

        super(Schedule, self).__init__()
        self._stop_event = threading.Event()

    def run(self):
        self.runSchedule()

    def __del__(self):
        logger.info('deleted')

    def runSchedule(self):
        try:
            logger.info(f'runSchedule start SCH_ID:{self.schId}')
            self.isRun = True

            if self.schjobTy == 'SEC':
                sleep_time = int(self.schJob)
            elif self.schjobTy == 'MIN':
                sleep_time = int(self.schJob) * 60
            elif self.schjobTy == 'HOUR':
                sleep_time = int(self.schJob) * 3600
            elif self.schjobTy is None:
                try:
                    cron = CronTab(self.schJob)
                    next_run = cron.next(default_utc=True)
                    sleep_time = next_run
                except Exception as e:
                    logger.error(f'Invalid cron expression: {self.schJob}')
                    return
            else:
                logger.error(f'Invalid SCH_JOB_TYPE: {self.schjobTy}')
                return

            while self.isRun:
                for _ in range(int(sleep_time * 10)):  # 100ms 간격으로 체크
                    if not self.isRun:
                        return
                    self.times.sleep(0.1)
                if self.isRun:
                    self.task()
                if self.schjobTy is None:
                    next_run = cron.next(default_utc=True)
                    sleep_time = next_run

        except Exception as e:
            logger.error(f'runSchedule Exception :: {e}')

    def task(self):
        try:
            bz = BzActivator(self.bzInfo)
            bz.daemon = True
            bz.start()
        except Exception as e:
            logger.error(f'BzSchedule task exception : {e}')
