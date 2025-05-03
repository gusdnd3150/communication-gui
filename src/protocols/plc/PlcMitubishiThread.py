

from conf.logconfig import *
import threading
import time
import traceback
import socket
from src.protocols.msg.FreeCodec import FreeCodec
from src.protocols.msg.LengthCodec import LengthCodec
from src.protocols.msg.JSONCodec import JSONCodec
from src.protocols.BzActivator2 import BzActivator2
from src.protocols.Client import Client
import conf.skModule as moduleData
from datetime import datetime
from src.protocols.sch.BzSchedule2 import BzSchedule2
from concurrent.futures import ThreadPoolExecutor
from pymcprotocol import Type3E

class PlcMitubishiThread(threading.Thread):

    initData = None
    socket = None
    reactor = None
    isRun = False
    isShutdown =  False
    skLogYn = False
    logger = None
    delimiter = b''
    bzSchList = []
    plcMaker = None
    commTy = None
    cpuTy = None
    plcIp = None
    plcPort = None
    executor = ThreadPoolExecutor(max_workers=1)
    #[('D30', 0, 10, bytearray(b'')), ('D60', 0, 10, bytearray(b''))]  (메모리,pos,length, 바이트)
    plcBuffer = []

    def __init__(self, data):
        self.initData = data
        self.plcId = data['PLC_ID']
        self.logger = setup_sk_logger(self.plcId)
        self.plcIp = data['PLC_IP']
        self.plcPort = int(data['PLC_PORT'])
        self.cpuTy = data['CPU_TY']

        if len(data.get('ADDR_LIST')) > 0 :
            for addr in data.get('ADDR_LIST'):
                self.plcBuffer.append((addr['ADDR'], addr['POS'],addr['LENGTH'],bytearray()))

        if data.get('COMM_TY') is not None:
            # "binary" or "ascii"
            self.commTy = data.get('COMM_TY')


        if (data.get('SK_LOG') is not None and data.get('SK_LOG') == 'Y'):
            self.skLogYn = True
        else:
            self.skLogYn = False

        super(PlcMitubishiThread, self).__init__()
        self._stop_event = threading.Event()


    def __del__(self):
        logger.info(f'Thread {self.plcId} is deleted')


    def run(self):
        # moduleData.mainInstance.addClientRow(self.initData)
        self.initClient()

    def stop(self):
        try:
            logger = logging.getLogger(self.plcId)
            # 모든 핸들러 제거
            handlers = logger.handlers[:]
            for handler in handlers:
                handler.close()
                logger.removeHandler(handler)
            # 로거 제거
            logging.getLogger(self.plcId).handlers = []


        except Exception as e:
            self.logger.error(f'PLC_ID:{self.plcId} Stop fail : {traceback.format_exc()}')
        finally:
            self.isRun = False
            self.isShutdown = True
            self._stop_event.set()
            # moduleData.mainInstance.deleteTableRow(self.plcId, 'list_run_client')


    def initClient(self):
        try:
            # MC 프로토콜 인스턴스 생성
            # plctype(str): connect PLC type. "Q", "L", "QnA", "iQ-L", "iQ-R"  , default = Q

            self.logger.info(f' {self.cpuTy}----{self.commTy}')
            mc = Type3E(self.cpuTy)
            # PLC 연결 설정
            # commtype =  "binary" or "ascii".(Default: "binary")
            mc.setaccessopt(commtype=self.commTy)  # Binary 모드 사용

            mc.connect(self.plcIp, self.plcPort)  # PLC의 IP 주소와 포트
            mc.timer = 30
            isCon = True
            writ = True
            # 쓰기
            while writ:
                try:
                    byte_data = 'tt'.encode('utf-8')
                    print("write data :", byte_data)
                    decimal_codes = [byte for byte in byte_data]
                    print("write 십진수 (from_bytes):", decimal_codes)
                    # 각 바이트를 8비트 이진수로 변환하여 리스트로 저장
                    binary_representation = [format(byte, '08b') for byte in byte_data]
                    # 이진수 문자열로 결합
                    binary_string = ''.join(binary_representation)
                    print("이진수 표현:", binary_string)
                    mc.batchwrite_wordunits(headdevice="B1B85", values=decimal_codes)
                    writ = False
                except:
                    time.sleep(2)

            # 읽기
            while isCon:
                try:
                    # D100번지부터 10개의 워드를 읽음
                    result = mc.batchread_wordunits(headdevice="B1B85", readsize=2)
                    byte_data_alt = b''.join(word.to_bytes(2, byteorder='big') for word in result)
                    print("read 십진수 (to_bytes):", str(byte_data_alt))
                    ascii_chars = [chr(num) for num in result]
                    print("read 데이터 (to_ascii):", str(ascii_chars))
                    isCon = False
                except:
                    time.sleep(2)


        except:
            self.logger.error(f'{self.plcId} initClient Exception : {traceback.format_exc()}')

            if self.isShutdown == False:
                time.sleep(4)
                self.initClient()






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