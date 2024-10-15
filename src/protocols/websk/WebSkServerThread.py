import traceback
from conf.logconfig import *
import threading
from src.protocols.msg.FreeCodec import FreeCodec
from src.protocols.msg.LengthCodec import LengthCodec
from src.protocols.msg.JSONCodec import JSONCodec
import conf.skModule as moduleData
from src.protocols.sch.BzSchedule2 import BzSchedule2
from src.protocols.BzActivator2 import BzActivator2
import asyncio
import websockets
from concurrent.futures import ThreadPoolExecutor

import time
from datetime import datetime

class WebSkServerThread(threading.Thread):
    initData = None
    skId = ''
    skIp = ''
    skPort = 0
    skRelVal = '/'
    socket = None
    loop = None
    isRun = False
    skLogYn = False
    codec = None
    delimiter = b''
    client_list = []
    bzKeep = None
    bzActive = None
    bzInActive = None
    bzIdleRead = None
    bzSch = None
    logger = None
    skGrp = None
    executor = ThreadPoolExecutor(max_workers=20)
    bzSchList = []
    server = None

    def __init__(self, data):
        self.initData = data
        self.skId = data['SK_ID']
        self.skIp = data['SK_IP']
        self.skPort = int(data['SK_PORT'])

        self.logger = setup_sk_logger(self.skId)
        self.logger.info(f'SK_ID:{self.skId} - initData : {data}')

        self.loop = asyncio.new_event_loop()

        if (data.get('SK_GROUP') is not None):
            self.skGrp = data['SK_GROUP']

        if self.initData['HD_TYPE'] == 'FREE':
            self.codec = FreeCodec(self.initData)
        elif self.initData['HD_TYPE'] == 'LENGTH':
            self.codec = LengthCodec(self.initData)
        elif self.initData['HD_TYPE'] == 'JSON':
            self.codec = JSONCodec(self.initData)

        if self.initData.get('RELATION_VAL') is not None and self.initData.get('RELATION_VAL') != '':
            self.skRelVal = self.initData.get('RELATION_VAL')

        if data.get('SK_LOG') is not None and data.get('SK_LOG') == 'Y':
            self.skLogYn = True

        if self.initData['SK_DELIMIT_TYPE'] != '':
            if self.initData['SK_DELIMIT_TYPE'] == 'NULL':
                self.delimiter = int('0x00', 16).to_bytes(1, byteorder='big')
            else:
                self.delimiter = int(self.initData['SK_DELIMIT_TYPE'], 16).to_bytes(1, byteorder='big')

        if data.get('BZ_EVENT_INFO') is not None:
            for index, bz in enumerate(data.get('BZ_EVENT_INFO')):
                if bz.get('BZ_TYPE') == 'KEEP':
                    self.bzKeep = bz
                elif bz.get('BZ_TYPE') == 'ACTIVE':
                    self.bzActive = bz
                elif bz.get('BZ_TYPE') == 'IDLE_READ':
                    self.bzIdleRead = bz
                elif bz.get('BZ_TYPE') == 'INACTIVE':
                    self.bzInActive = bz

        super(WebSkServerThread, self).__init__()
        self._stop_event = threading.Event()


    def __del__(self):
        self.logger.info(f'Thread {self.skId} is deleted')

    def run(self):
        self.initServer()

    def stop(self):
        try:
            logger = logging.getLogger(self.skId)
            handlers = logger.handlers[:]
            for handler in handlers:
                handler.close()
                logger.removeHandler(handler)
            logging.getLogger(self.skId).handlers = []

            async def closeServer():

                try:
                    for skid, channel, thread in self.client_list:
                        await channel.close()

                    self.loop.stop()

                    for task in asyncio.all_tasks(self.loop):
                        self.logger.info(f'task = {task}')
                        task.cancel()
                except:
                    logger.error(f'stop Server exception: {traceback.format_exc()}')
                finally:
                    self.loop.close()

            asyncio.run(closeServer())
        except Exception as e:
            self.logger.error(f'SK_ID:{self.skId} Stop fail exception : {traceback.format_exc()}')
        finally:
            self._stop_event.set()
            moduleData.mainInstance.deleteTableRow(self.skId, 'list_run_server')
            self.loop.close()

    def initServer(self):
        try:
            moduleData.mainInstance.addServerRow(self.initData)
            async def runServer():
                self.server = await websockets.serve(self.websocket_handler, self.skIp, self.skPort)
                await asyncio.gather(
                    asyncio.Future(),  # Run forever
                )
            self.loop.run_until_complete(runServer())
            self.loop.run_forever()
        except Exception:
            moduleData.mainInstance.deleteTableRow(self.skId, 'list_run_server')
            self.logger.error(f'WEB SOCKET SERVER Bind exception : SK_ID={self.skId}  : {traceback.format_exc()}')

    async def websocket_handler(self, wesk, path):
        bzSch = None
        chinfo = {
            'SK_ID': self.skId
            , 'SK_GROUP': self.skGrp
            , 'CHANNEL': wesk
            , 'LOGGER': self.logger
            , 'THREAD': self
            , 'PATH': path  # 웹소켓 한해 접속 URL 을 포함
        }
        client_info = (self.skId, wesk, self)
        self.client_list.append(client_info)
        moduleData.runChannels.append(client_info)
        moduleData.mainInstance.updateConnList()

        client_ip, client_port = wesk.remote_address
        logger.info(f"SK_ID:{self.skId} Client connected: IP={client_ip}, Port={client_port}")

        # ACTIVE 이벤트처리
        if self.bzActive is not None:
            avtive_dict = {**chinfo, **self.bzActive}
            self.logger.info(f'{self.skId} : [ACTIVE CHANNEL EVENT START]')
            self.threadPoolExcutor(BzActivator2(avtive_dict))

        # KEEP 처리
        if self.bzKeep is not None:
            keep_dict = {**chinfo, **self.bzKeep}
            self.logger.info(f'{self.skId} : [KEEP CHANNEL EVENT START]')
            bzSch = BzSchedule2(keep_dict)
            bzSch.daemon = True
            bzSch.start()
            self.bzSchList.append(bzSch)

        try:
            async for message in wesk:
                reciveBytes = message.encode('utf-8')
                try:
                    readBytesCnt = self.codec.concyctencyCheck(reciveBytes)
                    if readBytesCnt == 0:
                        self.logger.info(f'concyctence error : {reciveBytes}')
                        continue

                    if self.skLogYn:
                        decimal_string = ' '.join(str(byte) for byte in reciveBytes)
                        self.logger.info(f'SK_ID:{self.skId} read length : {readBytesCnt} decimal_string : [{decimal_string}]')

                    data = self.codec.decodeRecieData(reciveBytes)
                    data['TOTAL_BYTES'] = reciveBytes
                    reciveObj = {**chinfo, **data}
                    self.threadPoolExcutor(BzActivator2(reciveObj))
                except:
                    self.logger.error(f'websocket_handler error : {traceback.format_exc()}')
        except:
            self.logger.error(f'websocket_handler error : {traceback.format_exc()}')
        finally:
            if bzSch is not None:
                bzSch.stop()
                bzSch.join()

            # self.bzSchList.remove(bzSch)
            if bzSch in self.bzSchList:
                self.bzSchList.remove(bzSch)

            if client_info in self.client_list:
                self.client_list.remove(client_info)
            if client_info in moduleData.runChannels:
                moduleData.runChannels.remove(client_info)
            moduleData.mainInstance.updateConnList()


    def sendBytesToChannel(self, channel ,bytes):
        try:
            async def send(self, channel, bytes):
                try:
                    await channel.send(bytes)  # await 키워드를 사용하여 비동기 호출
                    if self.skLogYn:
                        decimal_string = ' '.join(str(byte) for byte in bytes)
                        self.logger.info(f'SK_ID:{self.skId} send bytes length : {len(bytes)} send_string:[{str(bytes)}] decimal_string : [{bytes}]')
                except Exception:
                    self.logger.error(f'sendBytesToChannel send exception :: {traceback.format_exc()}')
            asyncio.run_coroutine_threadsafe(send(self, channel, bytes),self.loop)
        except:
            self.logger.error(f'sendBytesToChannel exception :: {traceback.format_exc()}')

    def sendBytesToAllChannels(self, bytes):
        try:
            pass
        except:
            self.logger.error(f'sendBytesToAllChannels exception :: {traceback.format_exc()}')


    def sendMsgToChannel(self, channel, obj):
        try:
            sendBytes = self.codec.encodeSendData(obj)
            async def send(self):
                try:
                    await channel.send(sendBytes.decode('utf-8'))
                    if self.skLogYn:
                        decimal_string = ' '.join(str(byte) for byte in sendBytes)
                        self.logger.info(f'SK_ID:{self.skId} send bytes length : {len(sendBytes)} send_string:[{str(sendBytes)}] decimal_string : [{decimal_string}]')
                except Exception:
                    self.logger.error(f'sendMsgToAllChannels send exception :: {traceback.format_exc()}')
            asyncio.run_coroutine_threadsafe(send(self), self.loop)
        except:
            self.logger.error(f'sendMsgToChannel exception :: {traceback.format_exc()}')



    def sendMsgToAllChannels(self, obj):
        try:
            sendBytes = self.codec.encodeSendData(obj)
            async def send(self):
                try:
                    for skId, channel, thraed in self.client_list:
                        await channel.send(sendBytes.decode('utf-8'))
                        if self.skLogYn:
                            decimal_string = ' '.join(str(byte) for byte in sendBytes)
                            self.logger.info(
                                f'SK_ID:{self.skId} send bytes length : {len(sendBytes)} send_string:[{str(sendBytes)}] decimal_string : [{sendBytes}]')
                except Exception:
                    self.logger.error(f'sendMsgToAllChannels send exception :: {traceback.format_exc()}')

            asyncio.run_coroutine_threadsafe(send(self), self.loop)
        except:
            self.logger.error(f'sendMsgToAllChannels exception :: {traceback.format_exc()}')




    def threadPoolExcutor(self, instance):
        try:
            # start_time = time.time()
            futures = self.executor.submit(instance.run)
            # result = futures.result() #다른 스레드에 영향을 미침

            # 운영시 비권장 futures의 블락을 우회하기위해 스레드 선언
            # result_thread = threading.Thread(target=self.process_result, args=(futures, msg, start_time,))
            # result_thread.daemon = True
            # result_thread.start()
        except:
            self.logger.info(f'threadPoolExcutor exception : SK_ID:{self.skId} - {traceback.format_exc()}')

    def process_result(self, future, msg, start_time):
        try:
            result = future.result()
            # 결과를 처리하는 로직
            if self.skLogYn:
                end_time = time.time()
                start = datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')
                end = datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')
                # logger.info(f"----------- SK_ID: {self.skId} future Result: {result} and remain thread Que : {self.executor._work_queue}")
                self.logger.info(
                    f'----------- SK_ID: {self.skId} - {msg} begin:{start} end:{end} total time: {round(end_time - start_time, 4)}------------')
        except Exception as e:
            self.logger(f"Exception while processing result: {e}")