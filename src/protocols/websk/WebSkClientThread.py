import traceback
from conf.logconfig import *
import threading

import socket
from src.protocols.msg.FreeCodec import FreeCodec
from src.protocols.msg.LengthCodec import LengthCodec
from src.protocols.msg.JSONCodec import JSONCodec
import conf.skModule as moduleData
from src.protocols.sch.BzSchedule2 import BzSchedule2
from src.protocols.BzActivator2 import BzActivator2
import asyncio
import websockets
from aiohttp import web
from concurrent.futures import ThreadPoolExecutor
import weakref
import time
from datetime import datetime

class WebSkClientThread(threading.Thread):
    initData = None
    skId = ''
    skIp = ''
    skPort = 0
    skRelVal = '/'
    socket = None
    loop = None
    isRun = False
    isShutdown = False
    skLogYn = False
    codec = None
    delimiter = b''
    client_list = []
    bzKeep = None
    bzActive = None
    bzInActive = None
    bzIdleRead = None
    bzSch = None
    skGrp = None
    executor = ThreadPoolExecutor(max_workers=1)
    bzSchList = []
    CLIENT = None

    def __init__(self, data):
        self.initData = data
        self.skId = data['SK_ID']
        self.skIp = data['SK_IP']
        self.skPort = int(data['SK_PORT'])

        # self.loop = asyncio.get_event_loop()
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

        super(WebSkClientThread, self).__init__()
        self._stop_event = threading.Event()


    def __del__(self):
        logger.info(f'Thread {self.skId} is deleted')

    def run(self):
        moduleData.mainInstance.addClientRow(self.initData)

        try:
            # self.loop.run_until_complete(self.initClient())
            self.loop.run_until_complete(self.connection_loop())
            # self.loop.run_forever()
        except KeyboardInterrupt:
            print("Client interrupted.")
        finally:
            self.loop.run_until_complete(self.loop.shutdown_asyncgens())
            self.loop.close()
            moduleData.mainInstance.updateConnList()
            # self.socket.close()
            print("Event loop closed.")


    # def stop(self):
    #     try:
    #         logger = logging.getLogger(self.skId)
    #         handlers = logger.handlers[:]
    #         for handler in handlers:
    #             handler.close()
    #             logger.removeHandler(handler)
    #         logging.getLogger(self.skId).handlers = []
    #
    #         self.isShutdown = True
    #         async def cancel_all_tasks(websocket):
    #             try:
    #                 for skInfo in enumerate(self.client_list):
    #                     if skInfo in moduleData.runChannels:
    #                         moduleData.runChannels.remove(skInfo)
    #                 self.client_list.clear()
    #                 moduleData.mainInstance.updateConnList()
    #                 try:
    #                     await websocket.close()
    #                 except:
    #                     print(f'ddd : {traceback.print_exc()}')
    #             except:
    #                 print(f'ddd : {traceback.print_exc()}')
    #             finally:
    #                 self.isRun = False
    #                 self.loop.run_until_complete(self.loop.shutdown_asyncgens())
    #                 self.loop.close()
    #
    #         asyncio.run(cancel_all_tasks(self.socket))
    #     except Exception as e:
    #         logger.error(f'SK_ID:{self.skId} Stop fail exception : {traceback.format_exc()}')
    #     finally:
    #         moduleData.mainInstance.deleteTableRow(self.skId, 'list_run_client')
    #         self.loop.close()
    #         self._stop_event.set()


    def stop(self):
        self.isShutdown = True
        self.isRun = False

        async def _shutdown():
            try:
                if self.socket is not None:
                    await self.socket.close()
            finally:
                self.socket = None
                # connection_loop가 while 조건 보고 빠지게 됨

        # self.loop가 살아있을 때만 스케줄
        try:
            asyncio.run_coroutine_threadsafe(_shutdown(), self.loop)
            self.loop.call_soon_threadsafe(self.loop.stop)  # run_forever 쓰는 경우
        except Exception:
            logger.error(f"stop schedule error: {traceback.format_exc()}")

    async def initClient(self):
        """웹소켓 서버에 연결합니다. 성공 True / 실패 False"""
        url = f'ws://{self.skIp}:{self.skPort}'
        try:
            self.socket = await websockets.connect(url)
            self.isRun = True
            logger.info(f"Connected to server at {url}")
            return True
        except Exception as e:
            self.isRun = False
            logger.error(f"Failed to connect to {url}: {e}")
            return False


    async def websocket_handler(self):
        bzSch = None

        chinfo = {
            'SK_ID': self.skId
            , 'SK_GROUP': self.skGrp
            , 'CHANNEL': self.socket
            , 'THREAD': weakref.ref(self)
            # , 'PATH': path  # 웹소켓 한해 접속 URL 을 포함
        }
        client_info = (self.skId, self.socket, weakref.ref(self))
        self.client_list.append(client_info)
        moduleData.runChannels.append(client_info)
        moduleData.mainInstance.updateConnList()

        # client_ip, client_port = self.socket.remote_address
        # logger.info(f"SK_ID:{self.skId} Client connected: IP={client_ip}, Port={client_port}")

        # ACTIVE 이벤트처리
        if self.bzActive is not None:
            avtive_dict = {**chinfo, **self.bzActive}
            logger.info(f'{self.skId} : [ACTIVE CHANNEL EVENT START]')
            self.threadPoolExcutor(BzActivator2(avtive_dict))

        # KEEP 처리
        if self.bzKeep is not None:
            keep_dict = {**chinfo, **self.bzKeep}
            logger.info(f'{self.skId} : [KEEP CHANNEL EVENT START]')
            bzSch = BzSchedule2(keep_dict)
            bzSch.daemon = True
            bzSch.start()
            self.bzSchList.append(bzSch)

        try:
            while self.isRun:
                async for message in self.socket:
                    reciveBytes = message.encode('utf-8')
                    readBytesCnt = self.codec.concyctencyCheck(reciveBytes)
                    if readBytesCnt == 0:
                        logger.info(f'concyctence error : {reciveBytes}')
                        continue

                    if self.skLogYn:
                        decimal_string = ' '.join(str(byte) for byte in reciveBytes)
                        logger.info(
                            f'SK_ID:{self.skId} read length : {readBytesCnt} recive_string:[{str(reciveBytes)}] decimal_string : [{decimal_string}]')

                    data = self.codec.decodeRecieData(reciveBytes)
                    data['TOTAL_BYTES'] = reciveBytes
                    reciveObj = {**chinfo, **data}
                    self.threadPoolExcutor(BzActivator2(reciveObj))
        except:
            logger.error(f'websocket_handler error : {traceback.format_exc()}')
            moduleData.mainInstance.updateConnList()
            self.isRun = False
        finally:
            if bzSch is not None:
                bzSch.stop()
                bzSch.join()

            # self.bzSchList.remove(bzSch)
            if bzSch in self.bzSchList:
                self.bzSchList.remove(bzSch)

            if client_info in moduleData.runChannels:
                moduleData.runChannels.remove(client_info)
            if client_info in self.client_list:
                self.client_list.remove(client_info)

            moduleData.mainInstance.updateConnList()

            await self.socket.close()
            self.socket = None

            # if self.isShutdown == False:
            #     await self.initClient()
            # else:
            #     await self.socket.close()
            #     self.socket = None



    async def connection_loop(self):
        while not self.isShutdown:
            ok = await self.initClient()
            if not ok:
                await asyncio.sleep(5)
                continue
            try:
                # 여기서 핸들러를 "기다려"서 끊기면 다음 루프로
                await self.websocket_handler()
            except Exception:
                logger.error(f"connection_loop handler error: {traceback.format_exc()}")
            finally:
                # 소켓 정리(중복 close 방지)
                try:
                    if self.socket is not None:
                        await self.socket.close()
                except:
                    pass
                self.socket = None
                self.isRun = False

                if not self.isShutdown:
                    await asyncio.sleep(5)


    def sendBytesToChannel(self, channel ,bytes):
        try:
            async def send(self, channel, bytes):
                try:
                    await channel.send(bytes)  # await 키워드를 사용하여 비동기 호출
                    if self.skLogYn:
                        decimal_string = ' '.join(str(byte) for byte in bytes)
                        logger.info(f'SK_ID:{self.skId} send bytes length : {len(bytes)} send_string:[{str(bytes)}] decimal_string : [{bytes}]')
                except Exception:
                    logger.error(f'sendBytesToChannel send exception :: {traceback.format_exc()}')
            asyncio.run_coroutine_threadsafe(send(self, channel, bytes),self.loop)
        except:
            logger.error(f'sendBytesToChannel exception :: {traceback.format_exc()}')

    def sendBytesToAllChannels(self, bytes):
        try:
            async def send(self, bytes):
                try:
                    await self.socket.send(bytes)  # await 키워드를 사용하여 비동기 호출
                    if self.skLogYn:
                        decimal_string = ' '.join(str(byte) for byte in bytes)
                        logger.info(f'SK_ID:{self.skId} send bytes length : {len(bytes)} send_string:[{str(bytes)}] decimal_string : [{bytes}]')
                except Exception:
                    logger.error(f'sendBytesToChannel send exception :: {traceback.format_exc()}')

            asyncio.run_coroutine_threadsafe(send(self, bytes), self.loop)
        except:
            logger.error(f'sendBytesToAllChannels exception :: {traceback.format_exc()}')


    def sendMsgToChannel(self, channel, obj):
        try:
            sendBytes = self.codec.encodeSendData(obj)
            async def send(self):
                try:
                    await channel.send(sendBytes.decode('utf-8'))
                    if self.skLogYn:
                        decimal_string = ' '.join(str(byte) for byte in sendBytes)
                        logger.info(f'SK_ID:{self.skId} send bytes length : {len(sendBytes)} send_string:[{sendBytes.decode("utf-8", errors="replace")}] decimal_string : [{decimal_string}]')
                except Exception:
                    logger.error(f'sendMsgToAllChannels send exception :: {traceback.format_exc()}')
            asyncio.run_coroutine_threadsafe(send(self), self.loop)
        except:
            logger.error(f'sendMsgToChannel exception :: {traceback.format_exc()}')



    def sendMsgToAllChannels(self, obj):
        try:
            sendBytes = self.codec.encodeSendData(obj)
            async def send(self):
                try:
                    if self.socket is not None:
                        await self.socket.send(sendBytes.decode('utf-8'))
                        if self.skLogYn:
                            decimal_string = ' '.join(str(byte) for byte in sendBytes)
                            logger.info(
                                f'SK_ID:{self.skId} send bytes length : {len(sendBytes)} send_string:[{sendBytes.decode("utf-8", errors="replace")}] decimal_string : [{sendBytes}]')
                    else:
                        logger.error(f'{self.skId} has no Connection')
                except Exception:
                    logger.error(f'sendMsgToAllChannels send exception :: {traceback.format_exc()}')

            asyncio.run_coroutine_threadsafe(send(self), self.loop)
        except:
            logger.error(f'sendMsgToAllChannels exception :: {traceback.format_exc()}')




    def threadPoolExcutor(self, instance):
        try:
            # start_time = time.time()
            futures = self.executor.submit(instance.run)
            # result = futures.result() #다른 스레드에 영향을 미침

            # 운영시 비권장 futures의 블락을 우회하기위해 스레드 선언
            # if self.skLogYn:
            #     result_thread = threading.Thread(target=self.process_result, args=(futures, msg, start_time,))
            #     result_thread.daemon = True
            #     result_thread.start()
        except:
            logger.info(f'threadPoolExcutor exception : SK_ID:{self.skId} - {traceback.format_exc()}')

    def process_result(self, future, msg, start_time):
        try:
            result = future.result()
            end_time = time.time()
            start = datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')
            end = datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')
            # logger.info(f"----------- SK_ID: {self.skId} future Result: {result} and remain thread Que : {self.executor._work_queue}")
            logger.info(
                f'----------- SK_ID: {self.skId} - {msg} begin:{start} end:{end} total time: {round(end_time - start_time, 4)}------------')
        except Exception as e:
            logger(f"Exception while processing result: {e}")