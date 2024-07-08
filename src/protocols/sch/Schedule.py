
from conf.logconfig import logger
import threading

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
            
        except Exception as e:
            logger.info(f'runSchedule Exception :: {e}')
