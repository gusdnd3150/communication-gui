import traceback
from conf.logconfig import *
import threading
import socket
from src.protocols.msg.FreeCodec import FreeCodec
from src.protocols.msg.LengthCodec import LengthCodec
from src.protocols.msg.JSONCodec import JSONCodec
import conf.skModule as moduleData
from src.protocols.BzActivator2 import BzActivator2
from concurrent.futures import ThreadPoolExecutor, as_completed

import time
from datetime import datetime

class ServerUdpThread(threading.Thread):

    initData = None
    skId = ''
    skGrp = ''
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
    executor = ThreadPoolExecutor(max_workers=20)
    skclientTy = ''

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
        self.skclientTy = data['SK_CLIENT_TYPE']

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

        super(ServerUdpThread,self).__init__()
        self._stop_event = threading.Event()

    def __del__(self):
        logger.info(f'Thread {self.skId} is deleted')

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


            if self.socket:
                self.socket.close()

        except Exception as e:
            self.logger.error(f'SK_ID:{self.skId} Stop fail')
        finally:
            self.isRun = False
            self._stop_event.set()
            moduleData.mainInstance.deleteTableRow(self.skId, 'list_run_server')


    def initServer(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.bind((self.skIp, self.skPort))
            self.logger.info(f'UDP SERVER Start : SK_ID= {self.skId}, IP= {self.skIp}:{self.skPort} :: Thread ')
            self.isRun = True

            # 서버 테이블 인설트
            moduleData.mainInstance.addServerRow(self.initData)

            while self.socket:
                message, address = self.socket.recvfrom(self.initData.get('MAX_LENGTH'))
                # self.client_handler(message, address)
                t = threading.Thread(target=self.client_handler, args=(bytearray(message), address))
                t.daemon = True
                t.start()
        except Exception as e:
            self.logger.error(f'UDP SERVER Bind exception : SK_ID={self.skId}  : {traceback.format_exc()}')



    def client_handler(self,message,  address):
        try:
            self.logger.info(f' {self.skId} - CLIENT connected  IP/PORT : {address}')

            chinfo = {
                'SK_ID': self.skId
                , 'SK_GROUP': self.skGrp
                , 'CHANNEL': address
                , 'LOGGER': self.logger
                , 'THREAD': self
            }

            if self.skLogYn:
                decimal_string = ' '.join(str(byte) for byte in message)
                self.logger.info(f'SK_ID:{self.skId} read length : {len(message)} recive_string:[{str(message)}] decimal_string : [{decimal_string}]')
                moduleData.mainInstance.insertLog(self.skId, message, 'IN')

            copyButes = message.copy()
            data = self.codec.decodeRecieData(message)
            data['TOTAL_BYTES'] = copyButes

            reciveObj = {**chinfo, **data}
            self.threadPoolExcutor(BzActivator2(reciveObj), '[Processing Received Data]')
        except Exception as e:
            self.logger.info(f'UDP client_handler exception :  {traceback.format_exc()}')


    def threadPoolExcutor(self, instance, msg):
        try:
            start_time = time.time()
            futures = self.executor.submit(instance.run)
            # result = futures.result() #다른 스레드에 영향을 미침

            # 운영시 비권장 futures의 블락을 우회하기위해 스레드 선언
            result_thread = threading.Thread(target=self.process_result, args=(futures, msg, start_time,))
            result_thread.daemon = True
            result_thread.start()
        except:
            self.logger.info(f'threadPoolExcutor exception : SK_ID:{self.skId} - {traceback.format_exc()}')

    def process_result(self, future, msg, start_time):
        try:
            result = future.result()
            # 결과를 처리하는 로직
            if self.skLogYn:
                end_time = time.time()
                start = datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')
                end = datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')
                # logger.info(f"----------- SK_ID: {self.skId} future Result: {result} and remain thread Que : {self.executor._work_queue}")
                self.logger.info(
                    f'----------- SK_ID: {self.skId} - {msg} begin:{start} end:{end} total time: {round(end_time - start_time, 4)}------------')
        except Exception as e:
            self.logger(f"Exception while processing result: {e}")