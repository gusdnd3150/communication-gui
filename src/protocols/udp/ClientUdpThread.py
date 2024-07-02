import traceback
from conf.logconfig import *
import threading
import socket
from src.protocols.msg.FreeCodec import FreeCodec
from src.protocols.msg.LengthCodec import LengthCodec
from src.protocols.msg.JSONCodec import JSONCodec
from conf.InitData_n import systemGlobals
from src.protocols.BzActivator import BzActivator


class ClientUdpThread(threading.Thread):

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
    client_list = []
    bzKeep = None
    bzActive = None
    bzInActive = None
    bzIdleRead = None
    bzSch = None
    logger = None
    connCnt = 0
    sendBytes = bytearray

    def __init__(self, data):
        # {'PKG_ID': 'CORE', 'SK_ID': 'SERVER2', 'SK_GROUP': None, 'USE_YN': 'Y', 'SK_CONN_TYPE': 'SERVER',
        #  'SK_TYPE': 'UDP', 'SK_CLIENT_TYPE': 'KEEP', 'HD_ID': 'HD_FREE', 'SK_PORT': 5556, 'SK_IP': '0.0.0.0',
        #  'SK_DELIMIT_TYPE': '0x00', 'RELATION_VAL': None, 'SK_LOG': 'Y', 'HD_TYPE': 'FREE', 'MSG_CLASS': '',
        #  'MAX_LENGTH': 1024, 'MIN_LENGTH': 4, 'HD_LEN': 0}
        # 'BZ_EVENT_INFO': [{'PKG_ID': 'CORE', 'SK_GROUP': 'TEST', 'BZ_TYPE': 'KEEP', 'USE_YN': 'Y', 'BZ_METHOD': 'TestController.test', 'SEC': 5, 'BZ_DESC': None}]}

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

        super(ClientUdpThread,self).__init__()
        self._stop_event = threading.Event()

    def __del__(self):
        logger.info('deleted')

    def run(self):
        systemGlobals['mainInstance'].addClientRow(self.initData)

        # self.initServer()

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

            self.isRun = False
            if self.socket:
                self.socket.close()

        except Exception as e:
            self.logger.error(f'SK_ID:{self.skId} Stop fail')
        finally:
            self._stop_event.set()
            systemGlobals['mainInstance'].deleteTableRow(self.skId, 'list_run_client')


    def sendToAllChannels(self, msgBytes):
        try:
            self.logger.info(f'UDP CLIENT Start : SK_ID= {self.skId}, IP= {self.skIp}:{self.skPort} :: Thread ')
            udpClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sent = udpClient.sendto(msgBytes, (self.skIp, self.skPort))
            # data, server = sent.recvfrom(4096)
            if self.skLogYn:
                decimal_string = ' '.join(str(byte) for byte in msgBytes)
                self.logger.info(f'SK_ID:{self.skId} send bytes length : {len(msgBytes)} decimal_string : [{decimal_string}]')
        except Exception as e:
            self.logger.error(f'SK_ID:{self.skId}- sendToAllChannels Exception :: {e}')





