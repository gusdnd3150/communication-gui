

from conf.logconfig import *
import threading
import time
import traceback
import socket
from src.protocols.tcp.msg.FreeCodec import FreeCodec
from src.protocols.tcp.msg.LengthCodec import LengthCodec
from src.protocols.BzActivator import BzActivator
from conf.InitData_n import systemGlobals

class ClientThread(threading.Thread):

    initData = None
    skId = ''
    skIp = ''
    skPort = 0
    socket = None
    reactor = None
    isRun = False
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
        self.name = data['SK_ID'] + '-thread'  # 스레드 이름 설정
        self.skIp = data['SK_IP']
        self.skPort = int(data['SK_PORT'])

        self.logger = setup_sk_logger(self.skId)
        self.logger.info(f'SK_ID:{self.skId} - initData : {data}')

        if (self.initData['HD_TYPE'] == 'FREE'):
            self.codec = FreeCodec(self.initData)
        elif (self.initData['HD_TYPE'] == 'LENGTH'):
            self.codec = LengthCodec(self.initData)

        if (data.get('SK_LOG') is not None and data.get('SK_LOG') == 'Y'):
            self.skLogYn = True

        if (self.initData['SK_DELIMIT_TYPE'] != ''):
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
        super().__init__()


    def run(self):
        self.initClient()

    def initClient(self):
        buffer = bytearray()
        try:
            # 서버에 연결합니다.
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.skIp, int(self.skPort)))

            self.logger.info('TCP CLIENT Start : SK_ID={}, IP={}, PORT={}'.format(self.skId, self.skIp, self.skPort))

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
            # if self.bzKeep is not None:
                # self.bzSch = BzSchedule(self.bzKeep)
                # self.bzSch.daemon = True
                # self.bzSch.start()


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
                    self.isRun = False
                    if self.socket:
                        self.socket.close()
                        self.socket = None
                    self.logger.error(f'Exception :: {e}')
                    break


            if self.isRun == False:
                self.initClient()

        except ConnectionRefusedError as e:
            self.logger.error(f'TCP CLIENT SK_ID={self.skId}  exception : {e}')
            self.isRun = False

        except Exception as e:
            self.isRun = False
            self.logger.error(f'TCP CLIENT SK_ID={self.skId}  exception : {e}')

        finally:
            buffer.clear()
            if self.isRun == False:
                # 연결이 실패한 경우 잠시 대기 후 재시도
                if self.socket:
                    self.socket.close()
                    self.socket = None
                time.sleep(5)  # 5초 대기 후 재시도
                self.initClient()


    def sendToAllChannels(self, msgBytes):
        try:
            if self.socket is not None:
                self.socket.sendall(msgBytes)
            else:
                self.logger.info(f'SK_ID:{self.skId}- can"t send  sendToAllChannels  SERVER is None')

        except Exception as e:
            self.logger.error(f'SK_ID:{self.skId}- sendToAllChannels Exception :: {e}')