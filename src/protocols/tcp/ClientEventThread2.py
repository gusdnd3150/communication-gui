

from conf.logconfig import *
import threading
import traceback
import socket
from src.protocols.msg.FreeCodec import FreeCodec
from src.protocols.msg.LengthCodec import LengthCodec
from src.protocols.msg.JSONCodec import JSONCodec
from src.protocols.BzActivator2 import BzActivator2
import conf.skModule as moduleData

from src.protocols.sch.BzSchedule2 import BzSchedule2
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from datetime import datetime

class ClientEventThread(threading.Thread):

    initData = None
    skId = ''
    skGrp = ''
    skIp = ''
    skPort = 0
    socket = None
    reactor = None
    isRun = False
    isShutdown =  False
    skLogYn = False
    codec = None
    delimiter = b''
    bzKeep = None
    bzActive = None
    bzInActive = None
    bzIdleRead = None
    bzSch = None
    logger = None
    conCnt = 0
    skclientTy = ''
    sendData = bytearray
    bzSchList = []
    executor = ThreadPoolExecutor(max_workers=4)

    def __init__(self, data, msgData):
        # {'PKG_ID': 'CORE', 'SK_ID': 'SERVER2', 'SK_GROUP': None, 'USE_YN': 'Y', 'SK_CONN_TYPE': 'SERVER',
        #  'SK_TYPE': 'TCP', 'SK_CLIENT_TYPE': 'KEEP', 'HD_ID': 'HD_FREE', 'SK_PORT': 5556, 'SK_IP': '0.0.0.0',
        #  'SK_DELIMIT_TYPE': '0x00', 'RELATION_VAL': None, 'SK_LOG': 'Y', 'HD_TYPE': 'FREE', 'MSG_CLASS': '',
        #  'MAX_LENGTH': 1024, 'MIN_LENGTH': 4, 'HD_LEN': 0}
        # logger.info(f' ClientThread initData : {data}')
        self.initData = data
        self.skId = data['SK_ID']
        # self.name = data['SK_ID'] + '-thread'  # 스레드 이름 설정
        self.skIp = data['SK_IP']
        self.skPort = int(data['SK_PORT'])
        self.skclientTy = data['SK_CLIENT_TYPE']

        # self.logger = setup_sk_logger(self.skId)
        self.logger = logger
        self.logger.info(f'{threading.currentThread().getName()}')
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

        self.sendData = self.codec.encodeSendData(msgData)
        super(ClientEventThread, self).__init__()
        self._stop_event = threading.Event()

    def run(self):
        self.initClient()

    def __del__(self):
        logger.info(f'Thread {self.skId} is deleted')

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

            if self.bzSch is not None:
                self.bzSch.stop()
                self.bzSch.join()
                self.bzSch = None
        except Exception as e:
            self.logger.error(f'SK_ID:{self.skId} Stop fail : {traceback.format_exc()}')
        finally:
            moduleData.mainInstance.deleteTableRow(self.skId, 'list_run_client')


    def initClient(self):
        isRun = False
        buffer = bytearray()
        sockets = None

        client_info = None
        chinfo = None
        bzSch = None
        try:
            # 서버에 연결합니다.
            sockets = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sockets.connect((self.skIp, int(self.skPort)))
            sockets.sendall(self.sendData)
            isRun = True

            chinfo = {
                'SK_ID': self.skId
                , 'SK_GROUP': self.skGrp
                , 'CHANNEL': sockets
                , 'THREAD': self
                , 'LOGGER': self.logger
            }
            client_info = (self.skId, self.socket, self)
            moduleData.runChannels.append(client_info)
            moduleData.mainInstance.updateConnList()

            #2. 여기에 active 이벤트 처리
            if self.bzActive is not None:
                avtive_dict = {**chinfo, **self.bzActive}
                self.threadPoolExcutor(BzActivator2(avtive_dict), '[ACTIVE Channel]')


                # KEEP 처리
            if self.bzKeep is not None:
                combined_dict = {**chinfo, **self.bzKeep}
                bzSch = BzSchedule2(combined_dict)
                bzSch.daemon = True
                bzSch.start()
                # self.bzSchList.append(bzSch)


            # 1. IDLE 타임아웃 설정 (예: 5초)
            if self.bzIdleRead is not None:
                sockets.settimeout(self.bzIdleRead.get('SEC'))

            with sockets:
                while sockets:
                    try:
                        reciveBytes = sockets.recv(self.initData.get('MAX_LENGTH'))
                        if not reciveBytes:
                            break
                        buffer.extend(reciveBytes)

                        if (self.initData['MIN_LENGTH'] > len(buffer)):
                            continue

                        while sockets:
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
                                        f'SK_ID:{self.skId} read length : {len(readByte)} recive_string:[{str(readByte)}] decimal_string : [{decimal_string}]')
                                    moduleData.mainInstance.insertLog(self.skId, readByte, 'IN')

                                copybytes = readByte.copy()
                                data = self.codec.decodeRecieData(readByte)
                                data['TOTAL_BYTES'] = copybytes

                                reciveObj = {**chinfo, **data}
                                self.threadPoolExcutor(BzActivator2(reciveObj), '[Processing Received Data]')
                            except Exception as e:
                                traceback.print_exc()
                                self.logger.error(f'SK_ID:{self.skId} Msg convert Exception : {e}  {str(buffer)}')
                            finally:
                                del buffer[0:readBytesCnt]

                    except socket.timeout:
                        self.logger.error(f'SK_ID:{self.skId} - IDLE READ exception')
                        if self.bzIdleRead is not None:
                            idle_dict = {**chinfo, **self.bzIdleRead}
                            self.threadPoolExcutor(BzActivator2(idle_dict), '[IDLE read]')
                        continue
                    except Exception as e:
                        isRun = False
                        traceback.print_exc()
                        break
        except Exception as e:
            isRun = False
            self.logger.error(f'TCP CLIENT SK_ID={self.skId}  exception : {e}')
        finally:
            buffer.clear()

            if client_info in moduleData.runChannels:
                moduleData.runChannels.remove(client_info)
            moduleData.mainInstance.updateConnList()
            if bzSch is not None:
                bzSch.stop()
                bzSch.join()
                bzSch = None

            if sockets:
                sockets.close()
                sockets = None
            self.stop()




    def sendBytesToAllChannels(self, msgBytes):
        try:
            pass
            # self.logger.info(f'SK_ID:{self.skId}- sendBytesToAllChannels is None')
        except Exception as e:
            self.logger.error(f'SK_ID:{self.skId}- sendToAllChannels Exception :: {e}')


    def sendBytesToChannel(self,channel, bytes):
        try:
            channel.sendall(bytes + self.delimiter)
            if self.skLogYn:
                decimal_string = ' '.join(str(byte) for byte in bytes)
                self.logger.info(f'SK_ID:{self.skId} send bytes length : {len(bytes)} send_string:[{str(bytes)}] decimal_string : [{decimal_string}]')
                moduleData.mainInstance.insertLog(self.skId, bytes, 'OUT')
        except:
            self.logger.error(f'SK_ID:{self.skId}- sendMsgToChannel Exception :: {traceback.format_exc()}')



    def sendMsgToAllChannels(self, obj):
        try:
            pass

        except Exception as e:
            self.logger.info(f'SK_ID:{self.skId}- sendToAllChannels Exception :: {e}')

    def sendMsgToChannel(self, channel, obj):
        try:
            if channel:
                sendBytes = self.codec.encodeSendData(obj)
                channel.sendall(sendBytes)
                if self.skLogYn:
                    decimal_string = ' '.join(str(byte) for byte in sendBytes)
                    self.logger.info(f'SK_ID:{self.skId} send bytes length : {len(sendBytes)} send_string:[{str(sendBytes)}] decimal_string : [{decimal_string}]')
                    moduleData.mainInstance.insertLog(self.skId, sendBytes, 'OUT')
            else:
                self.logger.info(f'SK_ID:{self.skId}- sendMsgToChannel has no Server')

        except Exception as e:
            self.logger.info(f'SK_ID:{self.skId}- sendMsgToChannel Exception :: {e}')



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
                self.logger.info(f'----------- SK_ID: {self.skId} - {msg} begin:{start} end:{end} total time: {round(end_time - start_time, 4)}------------')
        except Exception as e:
            self.logger(f"Exception while processing result: {e}")
