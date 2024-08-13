

from conf.logconfig import *
import threading
import time
import traceback
import socket
from src.protocols.msg.FreeCodec import FreeCodec
from src.protocols.msg.LengthCodec import LengthCodec
from src.protocols.msg.JSONCodec import JSONCodec
from src.protocols.BzActivator import BzActivator
from src.protocols.Client import Client
import conf.skModule as moduleData

from src.protocols.sch.BzSchedule import BzSchedule

class ClientThread(threading.Thread, Client):

    initData = None
    skId = ''
    skGrp = ''
    skIp = ''
    skPort = 0
    socket = None
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

    def __init__(self, data):
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
        super(ClientThread, self).__init__()
        self._stop_event = threading.Event()

    def __del__(self):
        logger.info('deleted')

    def run(self):
        moduleData.mainInstance.addClientRow(self.initData)
        self.initClient()

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

            if self.socket:
                self.socket.close()

            if len(self.bzSchList) > 0:
                for item in self.bzSchList:
                    item.stop()
                    item.join()

        except Exception as e:
            self.logger.error(f'SK_ID:{self.skId} Stop fail : {traceback.format_exc()}')
        finally:
            self.isRun = False
            self.isShutdown = True
            self._stop_event.set()
            moduleData.mainInstance.deleteTableRow(self.skId, 'list_run_client')


    def initClient(self):
        moduleData.mainInstance.modClientRow(self.skId, 'CON_COUNT', '0')
        buffer = bytearray()
        connInfo = {}
        connInfo['SK_ID'] = self.skId
        connInfo['CONN_INFO'] = f"('{self.skIp}', {self.skPort})"
        bzSch = None
        client_info = None
        chinfo = None

        try:
            # 서버에 연결합니다.
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.skIp, int(self.skPort)))
            self.logger.info('TCP CLIENT Start : SK_ID={}, IP={}, PORT={}'.format(self.skId, self.skIp, self.skPort))

            chinfo = {
                'SK_ID': self.skId
                , 'SK_GROUP': self.skGrp
                , 'CHANNEL': self.socket
                , 'CODEC': self.codec
                , 'LOGGER': self.logger
            }
            client_info = (self.skId, self.socket, self.codec)
            moduleData.mainInstance.modClientRow(self.skId, 'CON_COUNT', '1')
            moduleData.runChannels.append(client_info)
            moduleData.mainInstance.addConnRow(connInfo)

            #2. 여기에 active 이벤트 처리
            if self.bzActive is not None:
                self.logger.info(f'SK_ID:{self.skId} - CHANNEL ACTIVE')
                combined_dict = {**chinfo, **self.bzActive}
                bz = BzActivator(combined_dict)
                bz.daemon = True
                bz.start()

                # KEEP 처리
            if self.bzKeep is not None:
                combined_dict = {**chinfo, **self.bzKeep}
                bzSch = BzSchedule(combined_dict)
                bzSch.daemon = True
                bzSch.start()
                self.bzSchList.append(bzSch)

            # 1. IDLE 타임아웃 설정 (예: 5초)
            if self.bzIdleRead is not None:
                self.socket.settimeout(self.bzIdleRead.get('SEC'))


            self.isRun = True
            with self.socket:
                while self.socket:
                    try:
                        reciveBytes = self.socket.recv(self.initData.get('MAX_LENGTH'))
                        if not reciveBytes:
                            break
                        buffer.extend(reciveBytes)

                        if (self.initData['MIN_LENGTH'] > len(buffer)):
                            continue

                        while self.socket:
                            readBytesCnt = self.codec.concyctencyCheck(buffer.copy())
                            if readBytesCnt == 0:
                                break
                            elif readBytesCnt > len(buffer):
                                break
                            readByte = buffer[:readBytesCnt]

                            try:
                                if self.skLogYn:
                                    decimal_string = ' '.join(str(byte) for byte in readByte)
                                    self.logger.info(
                                        f'SK_ID:{self.skId} read length : {readBytesCnt} recive_string:[{str(readByte)}] decimal_string : [{decimal_string}]')

                                copybytes = readByte.copy()
                                data = self.codec.decodeRecieData(readByte)
                                data['TOTAL_BYTES'] = copybytes

                                reciveObj = {**chinfo, **data}
                                bz = BzActivator(reciveObj)
                                bz.daemon = True
                                bz.start()
                            except Exception as e:
                                traceback.print_exc()
                                self.logger.error(f'SK_ID:{self.skId} Msg convert Exception : {e}  {str(buffer)}')
                            finally:
                                del buffer[0:readBytesCnt]

                    except socket.timeout:
                        self.logger.error(f'SK_ID:{self.skId} - IDLE READ exception')
                        if self.bzIdleRead is not None:
                            combined_dict = {**chinfo, **self.bzIdleRead}
                            bz = BzActivator(combined_dict)
                            bz.daemon = True
                            bz.start()
                        continue
                    except Exception as e:
                        traceback.print_exc()
                        self.isRun = False
                        break
        except Exception as e:
            self.isRun = False
            self.logger.error(f'TCP CLIENT SK_ID={self.skId}  exception : {e}')

        finally:
            buffer.clear()
            if client_info is not None:
                moduleData.runChannels.remove(client_info)
            moduleData.mainInstance.modClientRow(self.skId, 'CON_COUNT', '0')
            moduleData.mainInstance.deleteTableRow(connInfo['CONN_INFO'], 'list_conn')
            if self.socket:
                self.socket.close()
                self.socket = None

            if bzSch is not None:
                bzSch.stop()
                bzSch = None

            if self.isShutdown == False:
                time.sleep(5)  # 5초 대기 후 재시도
                self.initClient()


    def sendBytesToAllChannels(self, msgBytes):
        try:
            if self.socket is not None:
                self.socket.sendall(msgBytes)
                if self.skLogYn:
                    decimal_string = ' '.join(str(byte) for byte in msgBytes)
                    self.logger.info(f'SK_ID:{self.skId} send bytes length : {len(msgBytes)} send_string:[{str(msgBytes)}] decimal_string : [{decimal_string}]')
            else:
                self.logger.info(f'SK_ID:{self.skId}- can"t send  sendToAllChannels  SERVER is None')

        except Exception as e:
            self.logger.error(f'SK_ID:{self.skId}- sendToAllChannels Exception :: {e}')


    def sendBytesToChannel(self,channel, bytes):
        try:
            if self.skLogYn:
                decimal_string = ' '.join(str(byte) for byte in bytes)
                self.logger.info(f'SK_ID:{self.skId} send bytes length : {len(bytes)} send_string:[{str(bytes)}] decimal_string : [{decimal_string}]')
            channel.sendall(bytes)
        except:
            self.logger.error(f'SK_ID:{self.skId}- sendMsgToChannel Exception :: {traceback.format_exc()}')



    def sendMsgToAllChannels(self, obj):

        try:
            if self.socket is not None:
                sendBytes = self.codec.encodeSendData(obj)
                self.socket.sendall(sendBytes)
                if self.skLogYn:
                    decimal_string = ' '.join(str(byte) for byte in sendBytes)
                    self.logger.info(f'SK_ID:{self.skId} send bytes length : {len(sendBytes)} send_string:[{str(sendBytes)}] decimal_string : [{decimal_string}]')
            else:
                self.logger.info(f'SK_ID:{self.skId} has no connection')
        except Exception as e:
            self.logger.info(f'SK_ID:{self.skId}- sendToAllChannels Exception :: {e}')

    def sendMsgToChannel(self, channel, obj):
        try:

            if self.socket:
                sendBytes = self.codec.encodeSendData(obj)
                self.socket.sendall(sendBytes)

                if self.skLogYn:
                    decimal_string = ' '.join(str(byte) for byte in sendBytes)
                    self.logger.info(f'SK_ID:{self.skId} send bytes length : {len(sendBytes)} send_string:[{str(sendBytes)}] decimal_string : [{decimal_string}]')
            else:
                self.logger.info(f'SK_ID:{self.skId}- sendMsgToChannel has no Server')
        except Exception as e:
            self.logger.info(f'SK_ID:{self.skId}- sendMsgToChannel Exception :: {e}')