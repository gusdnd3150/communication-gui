

from conf.logconfig import logger
import threading
import time
import traceback
import socket

class SocketClient(threading.Thread):
    # PKG_ID
    # SK_ID
    # SK_GROUP
    # USE_YN
    # SK_CONN_TYPE
    # SK_TYPE
    # SK_CLIENT_TYPE
    # HD_ID
    # SK_PORT
    # SK_IP
    # SK_DELIMIT_TYPE
    # RELATION_VAL
    # WATCH_MSG_ID
    # SK_LAST_RECEIVE_DT
    # SK_LAST_SEND_DT
    # SK_DESC
    # SK_STAT
    # REG_ID
    # UPD_ID
    # REG_DT
    # UPD_DT
    # SK_LOG

    initData = {}
    skId = ''
    skIp = ''
    skPort = 0
    isRun = False
    tryCount= 0

    def __init__(self, data):
        self.initData = data
        self.skId = data['SK_ID']
        self.name = data['SK_ID']+'-thread'  # 스레드 이름 설정
        self.skIp = data['SK_IP']
        self.skPort = int(data['SK_PORT'])
        super().__init__()

    def initClient(self):
        logger.info('TCP Client Start : SK_ID={}, IP={}, PORT={}'.format(self.skId, self.skIp, self.skPort))
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.skIp, int(self.skPort)))
            self.tryCount = 0
            self.isRun = True
            logger.info('Connection Success :: SK_ID={} IP={}, PORT={}'.format(self.skId,self.skId, self.skPort))
            # 서버로 부터 메세지 받기
            while self.isRun:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                byte_array = bytearray(data)
                logger.info('recive Data :'+str(byte_array))
                # self.mainInstance.reciveSocketData(byte_array)

        except:
            logger.info('Connection Fail SK_ID={} IP={} PORT={} '.format(self.skId, self.skIp, self.skPort))
            self.client_socket = None
            self.isRun = False
            self.tryCount = self.tryCount + 1
            # logger.info('client connect try count :: ' + str(self.tryCount))
            time.sleep(5)
            logger.info('Retry connection SK_ID={} IP={} PORT={} '.format(self.skId, self.skIp, self.skPort))
            self.initClient()

    def run(self):
        self.initClient()
