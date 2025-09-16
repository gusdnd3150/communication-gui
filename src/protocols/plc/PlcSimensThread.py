

from conf.logconfig import *
import threading
import time
import traceback
from datetime import datetime
from src.protocols.sch.BzSchedule2 import BzSchedule2
from concurrent.futures import ThreadPoolExecutor
import snap7


class PlcSimensThread(threading.Thread):

    initData = None
    socket = None
    reactor = None
    isRun = False
    isShutdown =  False
    skLogYn = False
    plcMaker = None
    commTy = None
    addrAlias = None
    cpuTy = None
    plcIp = None
    plcPort = None
    client = None
    executor = ThreadPoolExecutor(max_workers=1)
    #[('D30', 0, 10, bytearray(b'')), ('D60', 0, 10, bytearray(b''))]  (메모리,pos,length, 바이트)
    plcBuffer = []

    def __init__(self, data):
        self.initData = data
        self.plcId = data['PLC_ID']
        self.plcIp = data['PLC_IP']
        self.plcPort = int(data['PLC_PORT'])
        self.cpuTy = data['CPU_TY']
        self.slot = int(data['SLOT'])
        self.rack = int(data['RACK'])
        self.client = snap7.client.Client()

        if len(data.get('ADDR_LIST')) > 0 :
            for addr in data.get('ADDR_LIST'):
                self.plcBuffer.append((addr['ADDR'], addr['POS'],addr['LENGTH'],addr['ADDR_ALIAS'],bytearray()))

        self.commTy = data.get('COMM_TY','binary')

        if (data.get('SK_LOG') is not None and data.get('SK_LOG') == 'Y'):
            self.skLogYn = True
        else:
            self.skLogYn = False

        super(PlcSimensThread, self).__init__()
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
        except Exception as e:
            self.logger.error(f'PLC_ID:{self.plcId} Stop fail : {traceback.format_exc()}')
        finally:
            self._stop_event.set()
            # moduleData.mainInstance.deleteTableRow(self.plcId, 'list_run_client')


    def initClient(self):
        logger.info(f'PLC id:{self.plcId}  {self.plcIp}, {self.rack}, {self.slot}, {self.plcPort}')
        while not self.isShutdown:
            try:
                # MC 프로토콜 인스턴스 생성
                # plctype(str): connect PLC type. "Q", "L", "QnA", "iQ-L", "iQ-R"  , default = Q
                if not self.client.get_connected():
                    self.client.connect(self.plcIp, self.rack, self.slot, self.plcPort) # 기본은 102 포트

                for (addr, startId, endId ,alias, data) in self.plcBuffer:
                    logger.info(f'{self.plcId} read data : {addr} {startId} {endId} {data} {alias}')
                    data = self.client.db_read(db_number=addr, start=startId, size=endId)

                # db_data = self.client.db_read(1, 0, 8)                       # DB1
                # m_data  = self.client.read_area(Areas.MK, 0, 0, 4)           # M 영역
                # i_data  = self.client.read_area(Areas.PE, 0, 0, 1)           # 입력(I)
                # q_data  = self.client.read_area(Areas.PA, 0, 0, 1)           # 출력(Q)

            except:
                logger.error(f'{self.plcId} initClient Exception : {traceback.format_exc()}')

            finally:
                time.sleep(0.3)











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