

from conf.logconfig import logger
import threading
import time
import traceback
import socket
from src.protocols.tcp.msg.FreeCodec import FreeCodec

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
        logger.info(f' ClientThread initData : {data}')
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
        logger.info('TCP Client Start : SK_ID={}, IP={}, PORT={}'.format(self.skId, self.skIp, self.skPort))
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.skIp, int(self.skPort)))
            self.tryCount = 0
            self.isRun = True
            logger.info('Connection Success :: SK_ID={} IP={}, PORT={}'.format(self.skId,self.skId, self.skPort))
            while self.isRun:
                try:

                    reciveBytes = self.socket.recv(self.initData.get('MAX_LENGTH'))
                    if not reciveBytes:
                        break
                    buffer.extend(reciveBytes)

                except Exception as e:
                    logger.info(f'handler Exception : {e}')


        except:
            logger.info('Connection Fail SK_ID={} IP={} PORT={} '.format(self.skId, self.skIp, self.skPort))
            self.client_socket = None
            self.isRun = False
            self.tryCount = self.tryCount + 1
            time.sleep(5)
            logger.info('Retry connection SK_ID={} IP={} PORT={} '.format(self.skId, self.skIp, self.skPort))
            self.initClient()


        buffer.clear()