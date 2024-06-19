
from conf.logconfig import logger
import threading

class Schedule(threading.Thread):
    initData = None

    def __init__(self):
        logger.info('run Schedule')
        super().__init__()
        self.name = 'Thread Schedule'


    def run(self):
        self.runSchedule()


    def runSchedule(self):
        try:
            logger.info(f'runSchedule start')


        except Exception as e:
            logger.info(f'runSchedule Exception :: {e}')
