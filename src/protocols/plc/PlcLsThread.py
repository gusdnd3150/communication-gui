import socket
import threading
import time
import traceback
import weakref
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from src.protocols.BzActivator2 import BzActivator2
from src.protocols.Client import Client
from src.protocols.msg.FreeCodec import FreeCodec
from src.protocols.msg.JSONCodec import JSONCodec
from src.protocols.msg.LengthCodec import LengthCodec
from src.protocols.sch.BzSchedule2 import BzSchedule2
import conf.skModule as moduleData
from conf.logconfig import *


class PlcLsThread(threading.Thread):
    initData = None
    socket = None
    reactor = None
    isRun = False
    isShutdown = False
    plcMaker = None
    commTy = None
    addrAlias = None
    cpuTy = None
    plcIp = None
    plcId = None
    plcPort = None
    client = None
    logYn = None
    executor = ThreadPoolExecutor(max_workers=1)
    # [('D30', 0, 10, bytearray(b'')), ('D60', 0, 10, bytearray(b''))]  (메모리,pos,length, 바이트)
    plcBuffer = []

    def __init__(self, data):
        self.initData = data
        self.plcId = data['PLC_ID']
        self.plcIp = data['PLC_IP']
        self.plcPort = int(data['PLC_PORT'])
        self.cpuTy = data['CPU_TY']
        self.slot = int(data['SLOT'])
        self.rack = int(data['RACK'])

        if len(data.get('ADDR_LIST')) > 0:
            for addr in data.get('ADDR_LIST'):
                self.plcBuffer.append((addr['ADDR'], addr['POS'], addr['LENGTH'], addr['ADDR_ALIAS'], bytearray()))

        self.commTy = data.get('COMM_TY', 'binary')

        if (data.get('LOG_YN') is not None and data.get('LOG_YN') == 'Y'):
            self.logYn = True
        else:
            self.logYn = False

        super(PlcLsThread, self).__init__()
        self._stop_event = threading.Event()

    def __del__(self):
        logger.info(f'Thread {self.plcId} is deleted')

    def run(self):
        # moduleData.mainInstance.addClientRow(self.initData)
        self.initClient()

    def stop(self):
        try:
            self.isRun = False
            self.isShutdown = True
            if self.client:
                self.client.close()
        except Exception as e:
            self.logger.error(f'PLC_ID:{self.plcId} Stop fail : {traceback.format_exc()}')
        finally:
            self._stop_event.set()

            # moduleData.mainInstance.deleteTableRow(self.plcId, 'list_run_client')

    def initClient(self):

        while not self.isShutdown:
            buffer = bytearray()
            bzSch = None
            conn_list = None
            channelInfo = None

            try:
                # 서버에 연결합니다.
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((self.plcIp, int(self.plcPort)))
                logger.info('PLC CLIENT Start : PLC_ID={}, IP={}, PORT={}'.format(self.plcId, self.plcIp, self.plcPort))

                channelInfo = {
                    'PLC_ID': self.plcId
                    , 'SK_GROUP': ''
                    , 'CHANNEL': self.socket
                    , 'THREAD': weakref.ref(self)
                }
                conn_list = (self.plcId, self.socket, weakref.ref(self))
                moduleData.runChannels.append(conn_list)  # 참조
                moduleData.mainInstance.updateConnList()

                self.socket.settimeout(10)

                self.isRun = True
                with self.socket:
                    while self.socket:
                        try:
                            reciveBytes = self.socket.recv(9999)
                            try:
                                if self.skLogYn:
                                    decimal_string = ' '.join(str(byte) for byte in reciveBytes)
                                    logger.info(
                                        f'PLC_ID:{self.plcId} recive_string:[{reciveBytes.decode("utf-8", errors="replace")}] decimal_string : [{decimal_string}] read length : {reciveBytessCnt} ')
                                # self.threadPoolExcutor(BzActivator2(reciveObj))
                            except Exception as e:
                                logger.error(f'PLC_ID:{self.plcId} Message parsing Exception : buffer= {str(buffer)} {e}')

                        except socket.timeout:
                            logger.info(f'{self.plcId} : [IDLE CHANNEL CLOSE]')
                            self.socket.close()
                            continue
                        except Exception as e:
                            logger.error(f'PLC_ID={self.plcId} connection exception : {traceback.format_exc()}')
                            self.isRun = False
                            break
            except Exception as e:
                self.isRun = False
                logger.error(f'PLC_ID={self.plcId}  TCP CLIENT try to connect exception : {e}')

            finally:
                if conn_list in moduleData.runChannels:
                    moduleData.runChannels.remove(conn_list)
                moduleData.mainInstance.updateConnList()

                if self.socket:
                    self.socket.close()
                    self.socket = None

                if self.isShutdown == False:
                    bzSch = None
                    conn_list = None
                    channelInfo = None
                    buffer = None
                    self.socket = None
                    time.sleep(5)  # 5초 대기 후 재시도


    def threadPoolExcutor(self, instance):
        try:
            futures = self.executor.submit(instance.run)
            # result = futures.result() #다른 스레드에 영향을 미침
        except:
            self.logger.info(f'threadPoolExcutor exception : PLC_ID:{self.plcId} - {traceback.format_exc()}')

    def process_result(self, future, msg, start_time):
        try:
            result = future.result()
            # 결과를 처리하는 로직
            if self.skLogYn:
                end_time = time.time()
                start = datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')
                end = datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')
                # logger.info(f"----------- PLC_ID: {self.plcId} future Result: {result} and remain thread Que : {self.executor._work_queue}")
                self.logger.info(
                    f'----------- PLC_ID: {self.plcId} - {msg} begin:{start} end:{end} total time: {round(end_time - start_time, 4)}------------')
        except Exception as e:
            self.logger(f"Exception while processing result: {e}")
