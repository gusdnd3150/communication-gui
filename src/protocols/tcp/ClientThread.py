

from conf.logconfig import *
import threading
import time
import traceback
import socket
from src.protocols.msg.FreeCodec import FreeCodec
from src.protocols.msg.LengthCodec import LengthCodec
from src.protocols.msg.JSONCodec import JSONCodec
from src.protocols.BzActivator import BzActivator
from conf.InitData_n import systemGlobals

from src.protocols.sch.BzSchedule import BzSchedule

class ClientThread(threading.Thread):

    initData = None
    skId = ''
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
    bzSch = None
    logger = None

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
        systemGlobals['mainInstance'].addClientRow(self.initData)
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


        except Exception as e:
            self.logger.error(f'SK_ID:{self.skId} Stop fail : {traceback.format_exc()}')
        finally:
            self.isRun = False
            self.isShutdown = True
            self._stop_event.set()
            systemGlobals['mainInstance'].deleteTableRow(self.skId, 'list_run_client')


    def initClient(self):
        systemGlobals['mainInstance'].modClientRow(self.skId, 'CON_COUNT', '0')
        buffer = bytearray()
        connInfo = {}
        connInfo['SK_ID'] = self.skId
        connInfo['CONN_INFO'] = f"('{self.skIp}', {self.skPort})"

        try:
            # 서버에 연결합니다.
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.skIp, int(self.skPort)))
            self.logger.info('TCP CLIENT Start : SK_ID={}, IP={}, PORT={}'.format(self.skId, self.skIp, self.skPort))

            if self.socket is not None:
                systemGlobals['mainInstance'].modClientRow(self.skId, 'CON_COUNT', '1')
                systemGlobals['mainInstance'].addConnRow(connInfo)


            #2. 여기에 active 이벤트 처리
            if self.bzActive is not None:
                self.logger.info(f'SK_ID:{self.skId} - CHANNEL ACTIVE')
                self.bzActive['SK_ID'] = self.skId
                self.bzActive['CHANNEL'] = self.socket
                self.bzActive['LOGGER'] = self.logger
                bz = BzActivator(self.bzActive)
                bz.daemon = True
                bz.start()

                # KEEP 처리
            if self.bzKeep is not None:
                self.bzKeep['SK_ID'] = self.skId
                self.bzKeep['CHANNEL'] = self.socket
                self.bzKeep['LOGGER'] = self.logger
                self.bzSch = BzSchedule(self.bzKeep)
                self.bzSch.daemon = True
                self.bzSch.start()


            # 1. IDLE 타임아웃 설정 (예: 5초)
            if self.bzIdleRead is not None:
                self.socket.settimeout(self.bzIdleRead.get('SEC'))

            self.isRun = True
            while self.isRun:
                try:
                    reciveBytes = self.socket.recv(self.initData.get('MAX_LENGTH'))
                    if not reciveBytes:
                        break
                    buffer.extend(reciveBytes)

                    if (self.initData['MIN_LENGTH'] > len(buffer)):
                        continue

                    while self.isRun:
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
                                    f'SK_ID:{self.skId} read length : {readBytesCnt} decimal_string : [{decimal_string}]')

                            data = self.codec.decodeRecieData(readByte)
                            data['TOTAL_BYTES'] = readByte.copy()
                            data['CHANNEL'] = self.socket
                            data['SK_ID'] = self.skId
                            data['LOGGER'] = self.logger
                            bz = BzActivator(data)
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
                        self.bzIdleRead['SK_ID'] = self.skId
                        self.bzIdleRead['CHANNEL'] = self.socket
                        self.bzIdleRead['LOGGER'] = self.logger
                        bz = BzActivator(self.bzIdleRead)
                        bz.daemon = True
                        bz.start()
                    continue
                except Exception as e:
                    traceback.print_exc()
                    self.isRun = False
                    break

        except ConnectionRefusedError as e:
            self.logger.error(f'TCP CLIENT SK_ID={self.skId}  exception : {e}')
            self.isRun = False

        except Exception as e:
            self.isRun = False
            self.logger.error(f'TCP CLIENT SK_ID={self.skId}  exception : {e}')

        finally:
            buffer.clear()
            systemGlobals['mainInstance'].modClientRow(self.skId, 'CON_COUNT', '0')
            systemGlobals['mainInstance'].deleteTableRow(connInfo['CONN_INFO'], 'list_conn')
            if self.socket:
                self.socket.close()
                self.socket = None

            if self.bzSch is not None:
                self.bzSch.stop()
                self.bzSch = None

            if self.isRun == False and self.isShutdown == False:
                time.sleep(5)  # 5초 대기 후 재시도
                self.initClient()


    def sendToAllChannels(self, msgBytes):
        try:
            if self.socket is not None:
                self.socket.sendall(msgBytes)
                if self.skLogYn:
                    decimal_string = ' '.join(str(byte) for byte in msgBytes)
                    self.logger.info(f'SK_ID:{self.skId} send bytes length : {len(msgBytes)} decimal_string : [{decimal_string}]')
            else:
                self.logger.info(f'SK_ID:{self.skId}- can"t send  sendToAllChannels  SERVER is None')

        except Exception as e:
            self.logger.error(f'SK_ID:{self.skId}- sendToAllChannels Exception :: {e}')