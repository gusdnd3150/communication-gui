import traceback
from conf.logconfig import *
import threading

import socket
from src.protocols.msg.FreeCodec import FreeCodec
from src.protocols.msg.LengthCodec import LengthCodec
from src.protocols.msg.JSONCodec import JSONCodec
from conf.InitData_n import systemGlobals

from src.protocols.sch.BzSchedule import BzSchedule
from src.protocols.BzActivator import BzActivator

import asyncio
import websockets

class WebSkServerThread(threading.Thread):
    initData = None
    skId = ''
    skIp = ''
    skPort = 0
    socket = None
    loop = None
    reactor = None
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

    def __init__(self, data):
        # {'PKG_ID': 'CORE', 'SK_ID': 'SERVER2', 'SK_GROUP': None, 'USE_YN': 'Y', 'SK_CONN_TYPE': 'SERVER',
        #  'SK_TYPE': 'TCP', 'SK_CLIENT_TYPE': 'KEEP', 'HD_ID': 'HD_FREE', 'SK_PORT': 5556, 'SK_IP': '0.0.0.0',
        #  'SK_DELIMIT_TYPE': '0x00', 'RELATION_VAL': None, 'SK_LOG': 'Y', 'HD_TYPE': 'FREE', 'MSG_CLASS': '',
        #  'MAX_LENGTH': 1024, 'MIN_LENGTH': 4, 'HD_LEN': 0}
        # 'BZ_EVENT_INFO': [{'PKG_ID': 'CORE', 'SK_GROUP': 'TEST', 'BZ_TYPE': 'KEEP', 'USE_YN': 'Y', 'BZ_METHOD': 'TestController.test', 'SEC': 5, 'BZ_DESC': None}]}

        self.initData = data
        self.skId = data['SK_ID']
        self.skIp = data['SK_IP']
        self.skPort = int(data['SK_PORT'])

        self.logger = setup_sk_logger(self.skId)
        self.logger.info(f'SK_ID:{self.skId} - initData : {data}')

        if (self.initData['HD_TYPE'] == 'FREE'):
            self.codec = FreeCodec(self.initData)
        elif (self.initData['HD_TYPE'] == 'LENGTH'):
            self.codec = LengthCodec(self.initData)
        elif (self.initData['HD_TYPE'] == 'JSON'):
            self.codec = JSONCodec(self.initData)

        if (data.get('SK_LOG') is not None and data.get('SK_LOG') == 'Y'):
            self.skLogYn = True

        if (self.initData['SK_DELIMIT_TYPE'] != ''):
            if (self.initData['SK_DELIMIT_TYPE'] == 'NULL'):
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
        logger.info('deleted')

    def run(self):
        self.initServer()



    def stop(self):
        try:
            logger = logging.getLogger(self.skId)
            # 모든 핸들러 제거
            handlers = logger.handlers[:]
            for handler in handlers:
                handler.close()
                logger.removeHandler(handler)
            # 로거 제거
            logging.getLogger(self.skId).handlers = []

            self.loop.call_soon_threadsafe(self.loop.stop)

        except Exception as e:
            self.logger.error(f'SK_ID:{self.skId} Stop fail')
        finally:
            self._stop_event.set()
            systemGlobals['mainInstance'].deleteTableRow(self.skId, 'list_run_server')

    def initServer(self):
        try:
            systemGlobals['mainInstance'].addServerRow(self.initData)
            self.logger.info(f'WEB SOCKET SERVER Start : SK_ID= {self.skId}, IP= {self.skIp}:{self.skPort} :: Thread ')
            self.logger.info(f"WebSocket server is running on ws://{self.skIp}:{self.skPort}")

            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            self.server = websockets.serve(self.client_handler, self.skIp, self.skPort)
            self.loop.run_until_complete(self.server)
            self.loop.run_forever()
        except Exception as e:
            self.logger.error(f'WEB SOCKET SERVER Bind exception : SK_ID={self.skId}  : {e}')

    async def client_handler(self, websocket, path):
        self.logger.error(f'SK_ID:{websocket}')
        client_info = (self.skId, websocket)
        self.client_list.append(client_info)
        try:
            async for message in websocket:
                reciveBytes = message.encode('utf-8')
                readBytesCnt = self.codec.concyctencyCheck(reciveBytes)
                if readBytesCnt == 0:
                    logger.info(f'concyctence error : {reciveBytes}')
                    break
                try:
                    if self.skLogYn:
                        decimal_string = ' '.join(str(byte) for byte in reciveBytes)
                        self.logger.info(
                            f'SK_ID:{self.skId} read length : {readBytesCnt} decimal_string : [{decimal_string}]')

                    data = self.codec.decodeRecieData(reciveBytes)
                    data['TOTAL_BYTES'] = reciveBytes
                    data['CHANNEL'] = websocket
                    data['SK_ID'] = self.skId
                    data['LOGGER'] = self.logger
                    bz = BzActivator(data)
                    bz.daemon = True
                    bz.start()
                except Exception as e:
                    traceback.print_exc()
                    self.logger.error(f'SK_ID:{self.skId} Msg convert Exception : {e}  {str(reciveBytes)}')
        except websockets.exceptions.ConnectionClosed:
            self.logger.error(f'close {websocket}')
        finally:
            self.client_list.remove(client_info)




                # await websocket.send(f"Echo: {message}")


    #
    def sendToAllChannels(self, bytes):
        try:
            logger.info(f'ssadasdaadasd')
            # await websocket.send(f"Echo: {message}")
            # if len(self.client_list) == 0:
            #     self.logger.info(f'sendToAllChannels -{self.skId} has no Clients')
            #     return
            # for skId, client in self.client_list:
            #     if skId == self.skId:
            #         client.sendall(bytes)
            #         if self.skLogYn:
            #             decimal_string = ' '.join(str(byte) for byte in bytes)
            #             self.logger.info(
            #                 f'SK_ID:{self.skId} send bytes length : {len(bytes)} decimal_string : [{decimal_string}]')

        except Exception as e:
            self.logger.info(f'SK_ID:{self.skId}- sendToAllChannels Exception :: {e}')

    def countChannelBySkId(self, skId):
        count = 0
        for skid, socket in self.client_list:
            if skid == skId:
                count += 1
        return count