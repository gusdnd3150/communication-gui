
from conf.logconfig import logger
import threading
from src.protocols.BzActivator import BzActivator


class Schedule(threading.Thread):

    bzInfo = None
    isRun = False
    schId = None
    schJob =None
    schjobTy = None

    def __init__(self, sch):
        self.initData = sch
        if sch.get('SCH_JOB') is not None:
            self.schJob = sch['SCH_JOB']

        if sch.get('SCH_JOB_TYPE') is not None:
            self.schjobTy = sch['SCH_JOB_TYPE']

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
            logger.info(f'BzSchedule start : SCH_ID = {self.schId} ')
            # self.schedule.every(self.interval).seconds.do(self.task)
            while self.isRun:
                # self.times.sleep(self.interval)
                # if self.isRun:
                #     self.task()
                for _ in range(int(self.interval * 10)):  # 100ms 간격으로 체크
                    if not self.isRun:
                        return
                    self.times.sleep(0.1)
                if self.isRun:
                    self.task()

        except Exception as e:
            logger.error(f'runSchedule Exception :: {e}')



 def task(self):
        try:
            bz = BzActivator(self.bzInfo)
            bz.daemon = True
            bz.start()
        except Exception as e:
            logger.error(f'BzSchedule task exception : {e}')
