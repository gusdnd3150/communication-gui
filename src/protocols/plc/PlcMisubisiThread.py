

from conf.logconfig import *
import threading
import time
import traceback
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from pymcprotocol import Type3E

class PlcMisubisiThread(threading.Thread):

    initData = None
    socket = None
    reactor = None
    isRun = False
    isShutdown =  False
    plcMaker = None
    commTy = None
    addrAlias = None
    cpuTy = None
    plcIp = None
    plcPort = None
    client = None
    logYn = None
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
        self.commTy = data.get('COMM_TY','binary')

        if len(data.get('ADDR_LIST')) > 0 :
            for addr in data.get('ADDR_LIST'):
                self.plcBuffer.append((addr['ADDR'], addr['POS'],addr['LENGTH'],addr['ADDR_ALIAS'],bytearray()))

        # for (addr, startId, endId ,alias, buff) in self.plcBuffer:
        #             logger.info(f'{self.plcId} read_data22 : {addr} {startId} {endId}  {alias} {buff}')

        # MC 프로토콜 기반, FX/Q/L 모두 Type3E 클래스로 처리 가능
        # self.client = Type3E(ascii=ascii_mode)
        self.client = Type3E()
        self.client.setaccessopt(commtype=self.commTy)

        if (data.get('LOG_YN') is not None and data['LOG_YN'] == 'Y'):
            self.logYn = True
        else:
            self.logYn = False

        super(PlcMisubisiThread, self).__init__()
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
        logger.info(f'PLC id:{self.plcId}  {self.plcIp}, {self.rack}, {self.slot}, {self.plcPort}')
        while not self.isShutdown:
            try:
                # MC 프로토콜 인스턴스 생성
                # plctype(str): connect PLC type. "Q", "L", "QnA", "iQ-L", "iQ-R"  , default = Q
                if not self.isRun:
                    # self.client.connect(self.plcIp, self.plcPort) # 기본은 102 포트
                    logger.info(f'{self.plcIp}:{self.plcPort} try to connect')
                    self.client.connect(self.plcIp, int(self.plcPort))
                    self.isRun = True

                # w_values = self.client.batchread_wordunits(headdevice=read_data, readsize=endId)
                # logger.info(f'{self.plcId} read_data : {w_values}')

                for (addr, startId, endId ,alias, data) in self.plcBuffer:
                    if self.logYn:
                        logger.info(f'{self.plcId} read_data22 : {addr} {startId} {endId}  {alias} {data}')
                    read_data = self.client.batchread_wordunits(addr, endId)
                    # self.plcBuffer[i] = (addr, startId, endId, alias, bytearray(read_data))
                    data = read_data
                    logger.info(f'{self.plcId} read_data22 : {data}')
            except:
                self.isRun = False
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