

from conf.logconfig import *
import threading
import time
import traceback
import socket
from src.protocols.msg.FreeCodec import FreeCodec
from src.protocols.msg.LengthCodec import LengthCodec
from src.protocols.msg.JSONCodec import JSONCodec
from src.protocols.BzActivator2 import BzActivator2
from src.protocols.Client import Client
import conf.skModule as moduleData
from datetime import datetime
from src.protocolsAsy.sch.BzSchedule import BzSchedule
from concurrent.futures import ThreadPoolExecutor

from src.protocolsAsy.BzActivator import BzActivator

import asyncio

class ClientAsync(Client):

    initData = None
    skId = ''
    skGrp = ''
    skIp = ''
    skPort = 0
    reactor = None
    isRun = False
    isShutdown =  False
    skLogYn = False
    codec = None
    delimiter = b''
    bzKeep = None
    bzActive = None
    bzInActive = None
    bzIdleRead = None
    logger = None
    bzSchList = []

    mainLoop = None


    def __init__(self, data, mainloop):
        # {'PKG_ID': 'CORE', 'SK_ID': 'SERVER2', 'SK_GROUP': None, 'USE_YN': 'Y', 'SK_CONN_TYPE': 'SERVER',
        #  'SK_TYPE': 'TCP', 'SK_CLIENT_TYPE': 'KEEP', 'HD_ID': 'HD_FREE', 'SK_PORT': 5556, 'SK_IP': '0.0.0.0',
        #  'SK_DELIMIT_TYPE': '0x00', 'RELATION_VAL': None, 'SK_LOG': 'Y', 'HD_TYPE': 'FREE', 'MSG_CLASS': '',
        #  'MAX_LENGTH': 1024, 'MIN_LENGTH': 4, 'HD_LEN': 0}
        # logger.info(f' ClientThread initData : {data}')
        self.initData = data
        self.skId = data['SK_ID']
        # self.name = data['SK_ID'] + '-thread'  # 스레드 이름 설정
        self.skIp = data['SK_IP']
        self.skPort = int(data['SK_PORT'])
        self.skclientTy = data['SK_CLIENT_TYPE']
        self.mainLoop = mainloop

        self.logger = setup_sk_logger(self.skId)
        self.logger.info(f'SK_ID:{self.skId} - initData : {data}')


        if (data.get('SK_GROUP') is not None):
            self.skGrp = data['SK_GROUP']

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
        # super().__init__()
        self._stop_event = threading.Event()

    def __del__(self):
        logger.info(f'Thread {self.skId} is deleted')


    def stop(self):
        try:
            self.logger.info(f'client stop test')
        except Exception as e:
            self.logger.error(f'SK_ID:{self.skId} Stop fail : {traceback.format_exc()}')
        finally:
            self.isRun = False
            self.isShutdown = True
            moduleData.mainInstance.deleteTableRow(self.skId, 'list_run_client')


    async def initClient(self):
        task = []
        conn_list = None
        try:
            reader, writer = await asyncio.open_connection(self.skIp, self.skPort)
            self.socket = writer
            self.isRun = True
            self.logger.info('TCP CLIENT Start : SK_ID={}, IP={}, PORT={}'.format(self.skId, self.skIp, self.skPort))
            chinfo = {
                'SK_ID': self.skId
                , 'SK_GROUP': self.skGrp
                , 'CHANNEL': self.socket
                , 'THREAD': self
                , 'LOGGER': self.logger
            }
            conn_list = (self.skId, self.socket, self)
            moduleData.runChannels.append(conn_list)
            moduleData.mainInstance.updateConnList()
            # self.socket.write(message.encode())
            # await writer.drain()  # 데이터가 전송될 때까지 대기 - 동기처리이기 때문에 패스

            # 송수신처리
            task.append(self.handler(reader, writer))

            # ACTIVE 처리
            if self.bzActive is not None:
                avtive_dict = {**chinfo, **self.bzActive}
                task.append(self.active(avtive_dict))

            # KEEP 처리
            if self.bzKeep is not None:
                combined_dict = {**chinfo, **self.bzKeep}
                task.append(self.keep(combined_dict))

            # 함수 일괄 실행
            await asyncio.gather(*task)

        except Exception as e:
            print(f"An error occurred: {e}")
            self.isRun = False

        finally:
            self.logger.info('TCP CLIENT disconnected : SK_ID={}, IP={}, PORT={}'.format(self.skId, self.skIp, self.skPort))

            if conn_list in moduleData.runChannels:
                moduleData.runChannels.remove(conn_list)

            moduleData.mainInstance.updateConnList()

            if self.isShutdown == False:
                await self.initClient()
            else:
                self.socket.close()
                await self.socket.wait_closed()  # 연결 닫기

    async def keep(self, keepInfo):
        try:
            self.logger.info(f'{self.skId} : [KEEP CHANNEL EVENT START]')
            instance = BzSchedule(keepInfo)
            await instance.run()
        except:
            self.logger.info(f'keep')

    async def active(self, bzInfo):
        try:
            self.logger.info(f'{self.skId} : [ACTIVE CHANNEL EVENT START]')
            instance = BzActivator(bzInfo)
            await instance.run()
        except:
            self.logger.info(f'keep')


    async def handler(self, reader, socket):
        buffer = bytearray()

        try:
            socket.write('test'.encode())

            while self.isRun:
                response = await reader.read(100)  # 서버의 응답을 기다림
                self.logger.info(f'reader :{reader}')
                if not response:
                    # 서버가 연결을 닫았을 때 종료
                    break

                self.logger.info(f"{self.skId} Received: {response.decode()}")
                # self.logger.info(f"Received: {type(response)}")
                buffer.extend(response)  # 응답을 버퍼에 추가
        except:
            print('ssss')

        finally:
            await asyncio.sleep(1)


    def sendBytesToAllChannels(self, msgBytes):
        try:
            async def send(self, bytes):
                try:
                    await self.socket.write(bytes)  # await 키워드를 사용하여 비동기 호출
                    if self.skLogYn:
                        decimal_string = ' '.join(str(byte) for byte in bytes)
                        self.logger.info(
                            f'SK_ID:{self.skId} send bytes length : {len(bytes)} send_string:[{str(bytes)}] decimal_string : [{bytes}]')
                except Exception:
                    self.logger.error(f'sendBytesToChannel send exception :: {traceback.format_exc()}')

            asyncio.run_coroutine_threadsafe(send(self, bytes), self.loop)
        except:
            self.logger.error(f'sendBytesToAllChannels exception :: {traceback.format_exc()}')


    def sendBytesToChannel(self,channel, bytes):
        try:
            sendBytes = bytes + self.delimiter
            channel.write(sendBytes)
            if self.skLogYn:
                decimal_string = ' '.join(str(byte) for byte in sendBytes)
                self.logger.info(f'SK_ID:{self.skId} send bytes length : {len(sendBytes)} send_string:[{str(sendBytes)}] decimal_string : [{decimal_string}]')

        except:
            self.logger.error(f'SK_ID:{self.skId}- sendMsgToChannel Exception :: {traceback.format_exc()}')



    def sendMsgToAllChannels(self, obj):

        try:
            if self.socket is not None:
                sendBytes = self.codec.encodeSendData(obj)
                self.socket.write(sendBytes)
                if self.skLogYn:
                    decimal_string = ' '.join(str(byte) for byte in sendBytes)
                    self.logger.info(f'SK_ID:{self.skId} send bytes length : {len(sendBytes)} send_string:[{str(sendBytes)}] decimal_string : [{decimal_string}]')
                    # moduleData.mainInstance.insertLog(self.skId, sendBytes, 'OUT')
            else:
                self.logger.info(f'SK_ID:{self.skId} has no connection')
        except Exception as e:
            self.logger.info(f'SK_ID:{self.skId}- sendToAllChannels Exception :: {traceback.format_exc()}')

    def sendMsgToChannel(self, channel, obj):
        try:

            if self.socket:
                sendBytes = self.codec.encodeSendData(obj)
                self.socket.write(sendBytes)

                if self.skLogYn:
                    decimal_string = ' '.join(str(byte) for byte in sendBytes)
                    self.logger.info(f'SK_ID:{self.skId} send bytes length : {len(sendBytes)} send_string:[{str(sendBytes)}] decimal_string : [{decimal_string}]')
                    # moduleData.mainInstance.insertLog(self.skId, sendBytes, 'OUT')
            else:
                self.logger.info(f'SK_ID:{self.skId}- sendMsgToChannel has no Server')
        except Exception as e:
            self.logger.info(f'SK_ID:{self.skId}- sendMsgToChannel Exception :: {e}')

