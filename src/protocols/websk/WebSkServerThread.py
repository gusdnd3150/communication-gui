import traceback
from conf.logconfig import *
import threading

import socket
from src.protocols.msg.FreeCodec import FreeCodec
from src.protocols.msg.LengthCodec import LengthCodec
from src.protocols.msg.JSONCodec import JSONCodec
import conf.skModule as moduleData
from src.protocols.sch.BzSchedule import BzSchedule
from src.protocols.BzActivator import BzActivator
from src.protocols import Server
import asyncio
import websockets
from aiohttp import web
from concurrent.futures import ThreadPoolExecutor

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
    executor = ThreadPoolExecutor(max_workers=4)

    def __init__(self, data):
        self.initData = data
        self.skId = data['SK_ID']
        self.skIp = data['SK_IP']
        self.skPort = int(data['SK_PORT'])

        self.logger = setup_sk_logger(self.skId)
        self.logger.info(f'SK_ID:{self.skId} - initData : {data}')

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
        self.logger.info('deleted')

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

            self.loop.call_soon_threadsafe(self.loop.stop)

            if self.bzSch is not None:
                self.bzSch.stop()
                self.bzSch.join()
                self.bzSch = None
        except Exception as e:
            self.logger.error(f'SK_ID:{self.skId} Stop fail')
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
            runner = web.AppRunner(app)
            self.loop.run_until_complete(runner.setup())
            server = web.TCPSite(runner, self.skIp, self.skPort)
            self.loop.run_until_complete(server.start())

            self.loop.run_forever()
        except Exception as e:
            self.logger.error(f'WEB SOCKET SERVER Bind exception : SK_ID={self.skId}  : {e}')

    async def websocket_handler(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        peername = request.transport.get_extra_info('peername')
        if peername:
            client_ip, client_port = peername
            logger.info(f"SK_ID:{self.skId} Client connected: IP={client_ip}, Port={client_port}")

        client_info = (self.skId, ws, self)
        self.client_list.append(client_info)
        moduleData.runChannels.append(client_info)
        moduleData.mainInstance.updateConnList()

        # ACTIVE 이벤트처리
        if self.bzActive is not None:
            self.logger.info(f'SK_ID:{self.skId} - CHANNEL ACTIVE')
            self.bzActive['SK_ID'] = self.skId
            self.bzActive['CHANNEL'] = ws
            self.bzActive['LOGGER'] = self.logger
            bz = BzActivator(self.bzActive)
            bz.daemon = True
            bz.start()

        # KEEP 처리
        if self.bzKeep is not None:
            self.bzKeep['SK_ID'] = self.skId
            self.bzKeep['CHANNEL'] = ws
            self.bzKeep['LOGGER'] = self.logger
            self.bzSch = BzSchedule(self.bzKeep)
            self.bzSch.daemon = True
            self.bzSch.start()

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
                    data['CHANNEL'] = ws
                    data['SK_ID'] = self.skId
                    data['LOGGER'] = self.logger
                    bz = BzActivator(data)
                    bz.daemon = True
                    bz.start()
                elif msg.type == web.WSMsgType.ERROR:
                    self.logger.error(f'SK_ID:{self.skId} Msg convert Exception : {ws.exception()}')

        except Exception as e:
            self.logger.error(f'SK_ID:{self.skId} exception : {traceback.format_exc()}')
        finally:
            if self.bzSch is not None:
                self.bzSch.stop()
                self.bzSch.join()
                self.bzSch = None

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
