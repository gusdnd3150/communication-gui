
from PySide6.QtCore import QThread, Signal, Slot
import asyncio
from conf.logconfig import logger
import traceback
from src.protocolsAsy.tcp.ClientAsync import ClientAsync
from src.protocolsAsy.tcp.ServerAsync import ServerAsync
import conf.skModule as moduleData
import threading


class MainThread(threading.Thread):

    mainLoop = None  # 메인 루프 생성
    skList = []
    mainLayout= None


    def __init__(self, mainLayout):
        super().__init__()


        self.mainLayout = mainLayout



    def run(self): # 백그라운드 작업 실행
        try:
            self.mainLoop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.mainLoop)

            tasks = []
            logger.info(f' Run Cnt : {len(moduleData.sokcetList)}')
            for i, item in enumerate(moduleData.sokcetList):
                skTy = item['SK_TYPE']
                skConTy = item['SK_CONN_TYPE']
                skClientTy = item['SK_CLIENT_TYPE']
                tasks.append(self.runSk(item,skTy,skConTy,skClientTy))
                self.mainLayout.handlPop.ui.combo_sk_list.addItem(item['SK_ID'])
                # if task is not None:
                #     self.mainLoop.get(task)  # 코루틴 실행

            # self.mainLoop.gather()
            # asyncio.gather()
            # self.mainLoop.run_until_complete(asyncio.gather(tasks))
            if tasks:  # tasks가 비어 있지 않은 경우에만 실행
                self.mainLoop.run_until_complete(asyncio.gather(*tasks))


            self.isRunSk = True
        except Exception as e:
            traceback.print_exc()
            logger.info(f'Init.start_sk() Exception :: {traceback.format_exc()}')



    async def runSk(self, info, sktype, skconntype, skclientty):
        try:
            if (sktype == 'TCP'):
                if (skconntype == 'SERVER'):
                    logger.info(f'ssss')
                elif (skconntype == 'CLIENT'):
                    if skclientty == 'KEEP':
                        asyncInfo = ClientAsync(info, self.mainLoop)
                        await asyncInfo.initClient()

            else:
                logger.info(f'None condition')

        except:
            traceback.print_exc()