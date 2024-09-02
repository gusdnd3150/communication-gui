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
from src.protocols import Server
import asyncio
import websockets
from aiohttp import web
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
    runner = None
    server = None


    def __init__(self, data):
        self.initData = data
        self.skId = data['SK_ID']
        self.skIp = data['SK_IP']
        self.skPort = int(data['SK_PORT'])

        self.logger = setup_sk_logger(self.skId)
        self.logger.info(f'SK_ID:{self.skId} - initData : {data}')

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

            if self.loop and self.loop.is_running():
                self.logger.info(f'Shutting down server: SK_ID= {self.skId}')

                async def close_client():
                    for skId, conn, thread in self.client_list:
                        await conn.close()

                # 서버 정지 및 애플리케이션 정리 비동기적으로 실행
                async def stop_server():
                    await self.server.stop()
                    await self.runner.cleanup()
                    self.loop.stop()  # 이벤트 루프 중지
                    # 이벤트 루프 종료
                    self.loop.close()

                close_client()
                # 비동기 작업을 이벤트 루프에서 실행
                self.loop.call_soon_threadsafe(lambda: asyncio.run_coroutine_threadsafe(stop_server(), self.loop))

                # 이벤트 루프가 중지될 때까지 기다림
                # self.loop.run_until_complete(self.loop.shutdown_asyncgens())

                if len(self.bzSchList) > 0:
                    for item in self.bzSchList:
                        item.stop()
                        item.join()

                # 모든 작업 완료 후 이벤트 루프 종료
                # self.loop.close()
                self.logger.info(f'Server stopped: SK_ID= {self.skId}')
            else:
                self.logger.info(f'No running loop to stop: SK_ID= {self.skId}')

        except Exception as e:
            self.logger.error(f'SK_ID:{self.skId} Stop fail exception : {traceback.format_exc()}')
        finally:
            self._stop_event.set()
            moduleData.mainInstance.deleteTableRow(self.skId, 'list_run_server')

    def initServer(self):
        try:
            moduleData.mainInstance.addServerRow(self.initData)
            self.logger.info(f'WEB SOCKET SERVER Start : SK_ID= {self.skId}, IP= {self.skIp}:{self.skPort} :: Thread ')
            self.logger.info(f"WebSocket server is running on ws://{self.skIp}:{self.skPort}/test")

            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)

            app = web.Application()
            app.router.add_get(self.skRelVal, self.websocket_handler)

            self.runner = web.AppRunner(app)
            self.loop.run_until_complete(self.runner.setup())
            self.server = web.TCPSite(self.runner, self.skIp, self.skPort)
            self.loop.run_until_complete(self.server.start())
            self.loop.run_forever()

        except Exception as e:
            self.logger.error(f'WEB SOCKET SERVER Bind exception : SK_ID={self.skId}  : {e}')

    async def websocket_handler(self, request):
        bzSch = None
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        peername = request.transport.get_extra_info('peername')

        if peername:
            client_ip, client_port = peername
            logger.info(f"SK_ID:{self.skId} Client connected: IP={client_ip}, Port={client_port}")

        chinfo = {
            'SK_ID': self.skId
            , 'SK_GROUP': self.skGrp
            , 'CHANNEL': ws
            , 'LOGGER': self.logger
            , 'THREAD': self
        }
        client_info = (self.skId, ws, self)
        self.client_list.append(client_info)
        moduleData.runChannels.append(client_info)
        moduleData.mainInstance.updateConnList()

        # ACTIVE 이벤트처리
        if self.bzActive is not None:
            avtive_dict = {**chinfo, **self.bzActive}
            self.threadPoolExcutor(BzActivator2(avtive_dict), '[ACTIVE Channel]')

        # KEEP 처리
        if self.bzKeep is not None:
            keep_dict = {**chinfo, **self.bzKeep}
            bzSch = BzSchedule2(keep_dict)
            bzSch.daemon = True
            bzSch.start()
            self.bzSchList.append(bzSch)

        try:
            async for msg in ws:
                if msg.type == web.WSMsgType.TEXT:
                    reciveBytes = msg.data.encode('utf-8')
                    readBytesCnt = self.codec.concyctencyCheck(reciveBytes)
                    if readBytesCnt == 0:
                        self.logger.info(f'concyctence error : {reciveBytes}')
                        break

                    if self.skLogYn:
                        decimal_string = ' '.join(str(byte) for byte in reciveBytes)
                        self.logger.info(
                            f'SK_ID:{self.skId} read length : {readBytesCnt} decimal_string : [{decimal_string}]')
                        # moduleData.mainInstance.insertLog(self.skId, reciveBytes, 'IN')

                    data = self.codec.decodeRecieData(reciveBytes)
                    data['TOTAL_BYTES'] = reciveBytes
                    reciveObj = {**chinfo, **data}
                    self.threadPoolExcutor(BzActivator2(reciveObj), '[Processing Received Data]')
                elif msg.type == web.WSMsgType.ERROR:
                    self.logger.error(f'SK_ID:{self.skId} Msg convert Exception : {ws.exception()}')

        except Exception as e:
            self.logger.error(f'SK_ID:{self.skId} exception : {traceback.format_exc()}')
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
        return ws

    async def idleRead(self, client, timeout):
        await asyncio.sleep(timeout)
        self.logger.info(f'Checking idle clients...')
        try:
            client.ping()
        except Exception as e:
            self.logger.error(f'Error pinging client: {e}')


    async def sendBytes(self, bytes):
        try:
            if len(self.client_list) == 0:
                self.logger.info(f'sendToAllChannels -{self.skId} has no Clients')
                return
            for skId, client, codec in self.client_list:
                if skId == self.skId:
                    json_string = bytes.decode('utf-8')
                    await client.send_str(json_string)
                    if self.skLogYn:
                        decimal_string = ' '.join(str(byte) for byte in bytes)
                        self.logger.info(f'SK_ID:{self.skId} send bytes length : {len(bytes)} decimal_string : [{decimal_string}]')
                        # moduleData.mainInstance.insertLog(self.skId, bytes, 'OUT')
        except Exception as e:
            self.logger.info(f'SK_ID:{self.skId}- sendToAllChannels Exception :: {e}')


    def sendBytesToChannel(self, channel ,bytes):
        try:
            async def send(self, channel, bytes):
                try:
                    await self.sendBytes(bytes)  # await 키워드를 사용하여 비동기 호출
                    # moduleData.mainInstance.insertLog(self.skId, bytes, 'OUT')
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
            pass
        except:
            self.logger.error(f'sendMsgToChannel exception :: {traceback.format_exc()}')



    def sendMsgToAllChannels(self, obj):
        try:
            sendBytes = self.codec.encodeSendData(obj)
            async def send(self):
                try:
                    await self.sendBytes(sendBytes)  # await 키워드를 사용하여 비동기 호출
                    # moduleData.mainInstance.insertLog(self.skId, sendBytes, 'OUT')
                except Exception:
                    self.logger.error(f'sendMsgToAllChannels send exception :: {traceback.format_exc()}')

            asyncio.run_coroutine_threadsafe(send(self), self.loop)
        except:
            self.logger.error(f'sendMsgToAllChannels exception :: {traceback.format_exc()}')

    def threadPoolExcutor(self, instance, msg):
        try:
            start_time = time.time()
            futures = self.executor.submit(instance.run)
            # result = futures.result() #다른 스레드에 영향을 미침

            # 운영시 비권장 futures의 블락을 우회하기위해 스레드 선언
            result_thread = threading.Thread(target=self.process_result, args=(futures, msg, start_time,))
            result_thread.daemon = True
            result_thread.start()
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