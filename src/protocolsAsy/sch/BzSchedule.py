
from conf.logconfig import logger
import threading
import traceback
import time
from src.protocolsAsy.BzActivator import BzActivator
import schedule
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
from concurrent.futures import ThreadPoolExecutor

class BzSchedule():

    bzInfo = None
    interval = None # 시간 간격 (초단위)
    logger = None
    isRun = False
    times = time
    schedule = None

    def __init__(self, bzInfo):
        # {'PKG_ID': 'CORE', 'SK_GROUP': 'TEST', 'BZ_TYPE': 'KEEP', 'USE_YN': 'Y', 'BZ_METHOD': 'TestController.test', 'SEC': None, 'BZ_DESC': None, 'CHANNEL':''}
        self.bzInfo = bzInfo
        self.interval = bzInfo['SEC']
        self.logger = bzInfo['LOGGER']
        self.logger.info(f'BzSchedule initData :{bzInfo}')

        self.schedule = schedule
        self.isRun = True
        self._stop_event = threading.Event()

    async def run(self):
        try:
            self.isRun = True
            self.schedule = AsyncIOScheduler()
            self.logger.info(f'BzSchedule start : SK_GROUP = {self.bzInfo["SK_GROUP"]} ')
            self.schedule.add_job(self.task, 'interval', seconds=self.interval)  # 2초 간격으로 비동기 작업 등록
            self.schedule.start()

            try:
                while self.isRun:
                    await asyncio.sleep(1)  # 메인 루프를 유지
            except (KeyboardInterrupt, SystemExit):
                self.schedule.shutdown()
        except Exception as e:
            self.isRun = False
            if self.schedule is not None:
                self.schedule.shutdown()

            self.logger.error(f'BzSchedule Exception :: {traceback.format_exc()}')

    def __del__(self):
        logger.info(f'Schedules Thread SK_GROUP = {self.bzInfo["SK_GROUP"]} is deleted')


    async def task(self):
        try:
            if self.isRun:
                isinstance = BzActivator(self.bzInfo)
                await isinstance.run()
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



