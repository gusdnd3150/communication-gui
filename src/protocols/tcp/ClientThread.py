

from conf.logconfig import logger
import threading
import time
import traceback
import socket
from src.protocols.tcp.msg.FreeCodec import FreeCodec
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

        if (self.initData['HD_TYPE'] == 'FREE'):
            self.codec = FreeCodec(self.initData)

        if (data.get('SK_LOG') is not None and data.get('SK_LOG') == 'Y'):
            self.skLogYn = True

        if (self.initData['SK_DELIMIT_TYPE'] != ''):
            self.delimiter = int(self.initData['SK_DELIMIT_TYPE'], 16).to_bytes(1, byteorder='big')
        super().__init__()


    def run(self):
        self.initClient()

    def initClient(self):
        buffer = bytearray()
        logger.info('TCP CLIENT Start : SK_ID={}, IP={}, PORT={}'.format(self.skId, self.skIp, self.skPort))

        try:
            # 서버에 연결합니다.
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.skIp, int(self.skPort)))

            #1. IDLE 타임아웃 설정 (예: 5초)
            # self.socket.settimeout(5)

            #2. 여기에 active 이벤트 처리
            logger.info('ACTIVE')

            self.isRun = True
            while self.isRun:
                try:
                    reciveBytes = self.socket.recv(self.initData.get('MAX_LENGTH'))
                    if not reciveBytes:
                        break
                    buffer.extend(reciveBytes)

                    if (self.initData['MIN_LENGTH'] > len(buffer)):
                        continue

                    reableLengthArr = self.codec.concyctencyCheck(buffer)

                    if (len(reableLengthArr) == 0):
                        logger.info(f'SK_ID: {self.skId} consystency False {str(buffer)}')
                        continue
                    logger.info(f'SK_ID: {self.skId} consystency True ')

                    for index, readLegnth in enumerate(reableLengthArr):
                        readByte = buffer[:readLegnth]
                        try:
                            totlaBytes = readByte.copy()
                            data = self.codec.decodeRecieData(readByte)
                            data['TOTAL_BYTES'] = totlaBytes
                            data['CHANNEL'] = self.socket

                            reciveThread = threading.Thread(target=self.onReciveData, args=(data,))
                            reciveThread.daemon = True
                            reciveThread.start()
                        except Exception as e:
                            logger.info(f'SK_ID:{self.skId} Msg convert Exception : {e}  {str(buffer)}')
                        finally:
                            del buffer[0:readLegnth]


                except socket.timeout:
                    logger.info(f'SK_ID:{self.skId} - IDLE READ exception')
                    continue
                except Exception as e:
                    self.isRun = False
                    if self.socket:
                        self.socket.close()
                        self.socket = None
                    logger.info(f'Exception :: {e}')
                    break


            if self.isRun == False:
                self.initClient()

        except ConnectionRefusedError as e:
            logger.info(f'TCP CLIENT SK_ID={self.skId}  exception : {e}')
            self.isRun = False

        except Exception as e:
            self.isRun = False
            logger.info(f'TCP CLIENT SK_ID={self.skId}  exception : {e}')

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
                logger.info(f'SK_ID:{self.skId}- can"t send  sendToAllChannels  SERVER is None')

        except Exception as e:
            logger.info(f'SK_ID:{self.skId}- sendToAllChannels Exception :: {e}')

    def onReciveData(self, data):
        try:
            # logger.info('onReciveData')
            if (data.get('IN_MSG_INFO') is not None):
                if (data.get('IN_MSG_INFO').get('BZ_METHOD') is not None):
                    bzClass = data.get('IN_MSG_INFO').get('BZ_METHOD')
                    classNm = bzClass.split('.')[0]
                    methdNm = bzClass.split('.')[1]
                    if classNm in systemGlobals:
                        my_class = systemGlobals[classNm]
                        method = getattr(my_class, methdNm)
                        if callable(method):
                            logger.info(f"onReciveData : {classNm}.{methdNm} call.")
                            method(data)
                        else:
                            logger.info(f"{methdNm} is not callable.")
                    else:
                        logger.info(f"Class {classNm} not found.")
                else:
                    logger.info(f'BZ_METHOD INFO is Null :')
                    return
            else:
                logger.info(f'IN_MSG_INFO INFO is Null :')
                return

        except Exception as e:
            traceback.logger.info_exc()
            logger.info(f'ClientHandler onReciveData() Exception :{e}')