

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
import weakref



class ClientThread(threading.Thread, Client):

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
    logger = None
    bzSchList = []
    executor = ThreadPoolExecutor(max_workers=1)

    def __init__(self, data):
        # {'PKG_ID': 'CORE', 'SK_ID': 'SERVER2', 'SK_GROUP': None, 'USE_YN': 'Y', 'SK_CONN_TYPE': 'SERVER',
        #  'SK_TYPE': 'TCP', 'SK_CLIENT_TYPE': 'KEEP', 'HD_ID': 'HD_FREE', 'SK_PORT': 5556, 'SK_IP': '0.0.0.0',
        #  'SK_DELIMIT_TYPE': '0x00', 'RELATION_VAL': None, 'SK_LOG': 'Y', 'HD_TYPE': 'FREE', 'MSG_CLASS': '',
        #  'MAX_LENGTH': 1024, 'MIN_LENGTH': 4, 'HD_LEN': 0}
        self.initData = data
        self.skId = data['SK_ID']
        self.skIp = data['SK_IP']
        self.skPort = int(data['SK_PORT'])
        self.logger = setup_sk_logger(self.skId)
        self.logger.info(f'SK_ID:{self.skId} - initData : {data}')
        self.skGrp = data.get('SK_GROUP',None)
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
        super(ClientThread, self).__init__()
        self._stop_event = threading.Event()

    def __del__(self):
        logger.info(f'Thread {self.skId} is deleted')
        self.cleanup()



    def run(self):
        moduleData.mainInstance.addClientRow(self.initData)
        self.initClient()

    def stop(self):
        try:
            self.isShutdown = True

            logger = logging.getLogger(self.skId)
            # 모든 핸들러 제거
            handlers = logger.handlers[:]
            for handler in handlers:
                handler.close()
                logger.removeHandler(handler)
            # 로거 제거
            logging.getLogger(self.skId).handlers = []
            
            if len(self.bzSchList) > 0:
                for item in self.bzSchList:
                    item.stop()
                    item.join()

            if self.socket:
                self.socket.close()
        except Exception as e:
            self.logger.error(f'SK_ID:{self.skId} Stop fail : {traceback.format_exc()}')
        finally:
            self.isRun = False
            self._stop_event.set()
            moduleData.mainInstance.deleteTableRow(self.skId, 'list_run_client')


    def cleanup(self):
        for key in list(self.__dict__.keys()):
            # logger.info(f'{key}')
            self.__dict__[key] = None


    def initClient(self):
        buffer = bytearray()
        
        bzSch = None
        conn_list = None
        channelInfo = None

        try:
            # 서버에 연결합니다.
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.skIp, int(self.skPort)))
            self.logger.info('TCP CLIENT Start : SK_ID={}, IP={}, PORT={}'.format(self.skId, self.skIp, self.skPort))

            channelInfo = {
                'SK_ID': self.skId
                , 'SK_GROUP': self.skGrp
                , 'CHANNEL': self.socket
                , 'THREAD': weakref.ref(self)
                , 'LOGGER': self.logger
            }
            conn_list = (self.skId, self.socket, weakref.ref(self))
            moduleData.runChannels.append(conn_list) # 참조
            moduleData.mainInstance.updateConnList() 

            #2. 여기에 active 이벤트 처리
            if self.bzActive is not None:
                avtive_dict = {**channelInfo, **self.bzActive}
                self.logger.info(f'{self.skId} : [ACTIVE CHANNEL EVENT START]')
                self.threadPoolExcutor(BzActivator2(avtive_dict))

                # KEEP 처리
            if self.bzKeep is not None:
                combined_dict = {**channelInfo, **self.bzKeep}
                self.logger.info(f'{self.skId} : [KEEP CHANNEL EVENT START]')
                bzSch = BzSchedule2(combined_dict)
                bzSch.daemon = True
                bzSch.start()
                self.bzSchList.append(bzSch)

            # 1. IDLE 타임아웃 설정 (예: 5초)
            if self.bzIdleRead is not None:
                self.socket.settimeout(self.bzIdleRead.get('SEC'))


            self.isRun = True
            with self.socket:
                while self.socket:
                    try:
                        reciveBytes = self.socket.recv(self.initData.get('MAX_LENGTH'))
                        if not reciveBytes:
                            break
                        buffer.extend(reciveBytes)

                        if (self.initData['MIN_LENGTH'] > len(buffer)):
                            continue
                        elif (self.initData['MAX_LENGTH'] < len(buffer)):
                            self.logger.info(f'maxLength reached {len(buffer)}')
                            buffer.clear()
                            continue

                        while self.socket:
                            readBytesCnt = self.codec.concyctencyCheck(buffer.copy())
                            if readBytesCnt == 0:
                                break
                            elif readBytesCnt > len(buffer):
                                break
                            readByte = buffer[:readBytesCnt]

                            try:
                                if self.skLogYn:
                                    decimal_string = ' '.join(str(byte) for byte in readByte)
                                    self.logger.info(f'SK_ID:{self.skId} recive_string:[{str(readByte)}] decimal_string : [{decimal_string}] read length : {readBytesCnt} ')

                                copybytes = readByte.copy()
                                data = self.codec.decodeRecieData(readByte)
                                data['TOTAL_BYTES'] = copybytes

                                reciveObj = {**channelInfo, **data}
                                self.threadPoolExcutor(BzActivator2(reciveObj))
                            except Exception as e:
                                self.logger.error(f'SK_ID:{self.skId} Message parsing Exception : buffer= {str(buffer)} {e}  ')
                            finally:
                                del buffer[0:readBytesCnt]

                    except socket.timeout:
                        if self.bzIdleRead is not None:
                            idle_dict = {**channelInfo, **self.bzIdleRead}
                            self.logger.info(f'{self.skId} : [IDLE CHANNEL EVENT START]')
                            self.threadPoolExcutor(BzActivator2(idle_dict))
                        continue
                    except Exception as e:
                        self.logger.error(f'SK_ID={self.skId} connection exception : {traceback.format_exc()}')
                        self.isRun = False
                        break
        except Exception as e:
            self.isRun = False
            self.logger.error(f'SK_ID={self.skId}  TCP CLIENT try to connect exception : {e}')

        finally:
            buffer.clear()
            if self.bzInActive is not None:
                inav_dict = {**channelInfo, **self.bzInActive}
                self.logger.info(f'{self.skId} : [INACTIVE CHANNEL EVENT START]')
                self.threadPoolExcutor(BzActivator2(inav_dict))

            if conn_list in moduleData.runChannels:
                moduleData.runChannels.remove(conn_list)
            moduleData.mainInstance.updateConnList()

            if bzSch is not None:
                bzSch.stop()
                bzSch.join()

            if bzSch in self.bzSchList:
                self.bzSchList.remove(bzSch)

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
                self.initClient()


    def sendBytesToAllChannels(self, msgBytes):
        try:
            if self.socket is not None:
                self.socket.sendall(msgBytes)
                if self.skLogYn:
                    decimal_string = ' '.join(str(byte) for byte in msgBytes)
                    self.logger.info(f'SK_ID:{self.skId} send bytes length : {len(msgBytes)} send_string:[{str(msgBytes)}] decimal_string : [{decimal_string}]')
                    # moduleData.mainInstance.insertLog(self.skId, msgBytes, 'OUT')
            else:
                self.logger.info(f'SK_ID:{self.skId}- can"t send  sendToAllChannels  SERVER is None')

        except Exception as e:
            self.logger.error(f'SK_ID:{self.skId}- sendToAllChannels Exception :: {e}')


    def sendBytesToChannel(self,channel, bytes):
        try:
            sendBytes = bytes + self.delimiter
            channel.sendall(sendBytes)
            if self.skLogYn:
                decimal_string = ' '.join(str(byte) for byte in sendBytes)
                self.logger.info(f'SK_ID:{self.skId} send bytes length : {len(sendBytes)} send_string:[{str(sendBytes)}] decimal_string : [{decimal_string}]')

        except:
            self.logger.error(f'SK_ID:{self.skId}- sendMsgToChannel Exception :: {traceback.format_exc()}')



    def sendMsgToAllChannels(self, obj):

        try:
            if self.socket is not None:
                sendBytes = self.codec.encodeSendData(obj)
                self.socket.sendall(sendBytes)
                if self.skLogYn:
                    decimal_string = ' '.join(str(byte) for byte in sendBytes)
                    self.logger.info(f'SK_ID:{self.skId} send bytes length : {len(sendBytes)} send_string:[{str(sendBytes)}] decimal_string : [{decimal_string}]')
                    # moduleData.mainInstance.insertLog(self.skId, sendBytes, 'OUT')
            else:
                self.logger.info(f'SK_ID:{self.skId} has no connection')
        except Exception as e:
            self.logger.info(f'SK_ID:{self.skId}- sendToAllChannels Exception :: {traceback.format_exc()}')

    def sendMsgToChannel(self, channel, obj):
        try:

            if self.socket:
                sendBytes = self.codec.encodeSendData(obj)
                self.socket.sendall(sendBytes)

                if self.skLogYn:
                    decimal_string = ' '.join(str(byte) for byte in sendBytes)
                    self.logger.info(f'SK_ID:{self.skId} send bytes length : {len(sendBytes)} send_string:[{str(sendBytes)}] decimal_string : [{decimal_string}]')
                    # moduleData.mainInstance.insertLog(self.skId, sendBytes, 'OUT')
            else:
                self.logger.info(f'SK_ID:{self.skId}- sendMsgToChannel has no Server')
        except Exception as e:
            self.logger.info(f'SK_ID:{self.skId}- sendMsgToChannel Exception :: {e}')

    def threadPoolExcutor(self, instance):
        try:
            # start_time = time.time()
            futures = self.executor.submit(instance.run)
            # result = futures.result() #다른 스레드에 영향을 미침

            # 운영시 비권장 futures의 블락을 우회하기위해 스레드 선언
            # result_thread = threading.Thread(target=self.process_result, args=(futures, msg, start_time,))
            # result_thread.daemon = True
            # result_thread.start()
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