
from conf.logconfig import logger
import threading

class BzSchedule(threading.Thread):
    initData = None

    def __init__(self):
        logger.info('run BzSchedule')
        super().__init__()
        self.name = 'Thread Schedule'

    def run(self):
        self.runSchedule()


    def runSchedule(self):
        try:
            logger.info(f'BzSchedule start')


        except Exception as e:
            logger.info(f'BzSchedule Exception :: {e}')