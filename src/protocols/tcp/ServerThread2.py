import traceback
from conf.logconfig import *
import threading

import socket
from src.protocols.msg.FreeCodec import FreeCodec
from src.protocols.msg.LengthCodec import LengthCodec
from src.protocols.msg.JSONCodec import JSONCodec
import conf.skModule as moduleData

from src.protocols.sch.BzSchedule2 import BzSchedule2
from src.protocols.BzActivator2 import BzActivator2
from src.protocols.Server import Server
from concurrent.futures import ThreadPoolExecutor
import time
from datetime import datetime

class ServerThread2(threading.Thread, Server):

    initData = None
    skId = ''
    skGrp = ''
    skIp = ''
    skPort = 0
    socket = None
    isRun = False
    skLogYn = False
    codec = None
    delimiter = b''
    conn_list = []
    bzKeep = None
    bzActive = None
    bzInActive = None
    bzIdleRead = None
    bzSchList = []
    logger = None
    executor = ThreadPoolExecutor(max_workers=100)
    skclientTy = ''


    def __init__(self, data):
        # {'PKG_ID': 'CORE', 'SK_ID': 'SERVER2', 'SK_GROUP': None, 'USE_YN': 'Y', 'SK_CONN_TYPE': 'SERVER',
        #  'SK_TYPE': 'TCP', 'SK_CLIENT_TYPE': 'KEEP', 'HD_ID': 'HD_FREE', 'SK_PORT': 5556, 'SK_IP': '0.0.0.0',
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

        super(ServerThread2,self).__init__()
        self._stop_event = threading.Event()

    def __del__(self):
        self.logger.info(f'Thread {self.skId} is deleted')

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

            if len(self.conn_list) > 0:
                for skId, client, thread in self.conn_list:
                    try:
                        client.close()
                    except:
                        self.logger.error(f'SK_ID:{self.skId} disConnected Client : {client}')

            if len(self.bzSchList) > 0:
                for item in self.bzSchList:
                    item.stop()
                    item.join()


            self.socket.close() # 완전 종료
        except Exception as e:
            self.logger.error(f'SK_ID:{self.skId} Stop fail : {traceback.format_exc()}')
        finally:
            self.isRun = False
            self._stop_event.set()
            moduleData.mainInstance.deleteTableRow(self.skId, 'list_run_server')



    def initServer(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((self.skIp, self.skPort))
            self.socket.listen(2000) #연결수 설정
            self.logger.info(f'TCP SERVER Start : SK_ID= {self.skId}, IP= {self.skIp}:{self.skPort} :: Thread ')
            self.isRun = True

            # 서버 테이블 인설트
            moduleData.mainInstance.addServerRow(self.initData)
            with self.socket:
                while self.socket:
                    (clientsocket, address) = self.socket.accept()
                    t = threading.Thread(target=self.client_handler, args=(clientsocket, address))
                    t.daemon = True
                    t.start()
        except Exception as e:
            self.logger.error(f'TCP SERVER Bind exception : SK_ID={self.skId}  : {e}')
        finally:
            self.socket.close()



    def client_handler(self,clientsocket, address):
        buffer = bytearray()
        # 공통  sk_id, channel, codec, thread
        client_info = (self.skId, clientsocket , self)
        self.conn_list.append(client_info) # 해당 소켓의 연결된 리스트

        moduleData.runChannels.append(client_info) # 전체
        moduleData.mainInstance.updateConnList()  # 연결 트리에 연결정보 추가
        # moduleData.insertConnHis(self.skId,client_info,'connected')

        bzSch = None
        chinfo = {
            'SK_ID': self.skId
            ,'SK_GROUP': self.skGrp
            , 'CHANNEL': clientsocket
            , 'LOGGER': self.logger
            , 'THREAD': self
        }
        self.logger.info(f' {self.skId} - CLIENT connected  IP/PORT : {address}')

        try:
            # ACTIVE 이벤트처리
            if self.bzActive is not None:
                avtive_dict = {**chinfo, **self.bzActive}
                self.threadPoolExcutor(BzActivator2(avtive_dict), '[ACTIVE Channel]')


            # KEEP 처리
            if self.bzKeep is not None:
                keep_dict = {**chinfo, **self.bzKeep}
                bzSch = BzSchedule2(keep_dict)
                bzSch.daemon = True
                bzSch.start()
                self.bzSchList.append(bzSch)


            # IDLE_READ 처리
            if self.bzIdleRead is not None:
                clientsocket.settimeout(self.bzIdleRead.get('SEC'))

            with clientsocket:
                while clientsocket:
                    try:
                        reciveBytes = clientsocket.recv(self.initData.get('MAX_LENGTH'))
                        if not reciveBytes:
                            break
                        buffer.extend(reciveBytes)

                        if (self.initData['MIN_LENGTH'] > len(buffer)):
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
                                    self.logger.info(f'SK_ID:{self.skId} read length : {len(readByte)} recive_string:[{str(readByte)}] decimal_string : [{decimal_string}]')
                                    # moduleData.mainInstance.insertLog(self.skId, readByte ,'IN')

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

                    except socket.timeout as e:
                        # self.logger.error(f'SK_ID:{self.skId}- IDLE READ exception : {e}')
                        if self.bzIdleRead is not None:
                            idle_dict = {**chinfo, **self.bzIdleRead}
                            self.threadPoolExcutor(BzActivator2(idle_dict), '[IDLE read]')

                    except Exception as e:
                        decimal_string = ' '.join(str(byte) for byte in buffer)
                        self.logger.error(f'SK_ID:{self.skId} handler Exception read length : {len(buffer)} decimal_string : [{decimal_string}]')
                        self.logger.error(f'SK_ID:{self.skId} handler Exception : {traceback.format_exc()}')
                        buffer.clear()
                        break

            # 버퍼 클리어
            buffer.clear()

            # inactive 처리
            self.logger.info(f'SK_ID:{self.skId}- CLIENT disConnected  IP/PORT : {address}')
            if self.bzInActive is not None:
                inav_dict = {**chinfo, **self.bzInActive}
                self.threadPoolExcutor(BzActivator2(inav_dict), '[INAVTIVE Channel]')

            if bzSch is not None:
                bzSch.stop()
                bzSch.join()

            # self.bzSchList.remove(bzSch)
            if bzSch in self.bzSchList:
                self.bzSchList.remove(bzSch)

            if clientsocket:
                if client_info in self.conn_list:
                    self.conn_list.remove(client_info)
                if client_info in moduleData.runChannels:
                    moduleData.runChannels.remove(client_info)

                self.logger.info(f'moduleData.runChannels : {moduleData.runChannels}')
                self.logger.info(f'SK_ID:{self.skId} remain Clients count {len(self.conn_list)})')
                clientsocket.close()
        except:

            self.logger.error(f'SK_ID:{self.skId} excepton : {traceback.format_exc()}')
            if clientsocket:
                clientsocket.close()

        finally:
                if client_info in self.conn_list:
                    self.conn_list.remove(client_info)
                if client_info in moduleData.runChannels:
                    moduleData.runChannels.remove(client_info)
                moduleData.mainInstance.updateConnList()

    def sendBytesToAllChannels(self, bytes):
        try:
            if len(self.conn_list) == 0:
                self.logger.info(f'sendToAllChannels -{self.skId} has no Clients')
                return
            for skId, client, codec in self.conn_list:
                if skId == self.skId:
                    client.sendall(bytes)
                    if self.skLogYn:
                        decimal_string = ' '.join(str(byte) for byte in bytes)
                        self.logger.info(f'SK_ID:{self.skId} send bytes length : {len(bytes)} send_string:[{str(bytes)}] decimal_string : [{decimal_string}]')

                        # moduleData.mainInstance.insertLog(self.skId, bytes, 'OUT')

        except Exception as e:
            self.logger.info(f'SK_ID:{self.skId}- sendToAllChannels Exception :: {e}')


    def sendBytesToChannel(self,channel, bytes):
        try:
            if self.skLogYn:
                decimal_string = ' '.join(str(byte) for byte in bytes)
                self.logger.info(f'SK_ID:{self.skId} send bytes length : {len(bytes)} send_string:[{str(bytes)}] decimal_string : [{decimal_string}]')
            channel.sendall(bytes)
            # moduleData.mainInstance.insertLog(self.skId, bytes, 'OUT')
        except:
            self.logger.error(f'SK_ID:{self.skId}- sendMsgToChannel Exception :: {traceback.format_exc()}')



    def sendMsgToAllChannels(self, obj):

        try:
            if len(self.conn_list) == 0:
                self.logger.info(f'sendToAllChannels -{self.skId} has no Clients')
                return
            sendBytes = self.codec.encodeSendData(obj)

            for skId, client, thread in self.conn_list:
                if skId == self.skId:
                    client.sendall(sendBytes)
                    if self.skLogYn:
                        decimal_string = ' '.join(str(byte) for byte in sendBytes)
                        self.logger.info(
                            f'SK_ID:{self.skId} send bytes length : {len(sendBytes)} send_string:[{str(sendBytes)}] decimal_string : [{decimal_string}]')
                        # moduleData.mainInstance.insertLog(self.skId, sendBytes, 'OUT')

        except Exception as e:
            self.logger.info(f'SK_ID:{self.skId}- sendToAllChannels Exception :: {e}')

    def sendMsgToChannel(self, channel, obj):

        try:
            if len(self.conn_list) == 0:
                self.logger.info(f'sendToAllChannels -{self.skId} has no Clients')
                return
            sendBytes = self.codec.encodeSendData(obj)
            channel.sendall(sendBytes)
            if self.skLogYn:
                decimal_string = ' '.join(str(byte) for byte in sendBytes)
                self.logger.info(f'SK_ID:{self.skId} send bytes length : {len(sendBytes)} send_string:[{str(sendBytes)}] decimal_string : [{decimal_string}]')

                # moduleData.mainInstance.insertLog(self.skId, sendBytes)
                # moduleData.mainInstance.insertLog(self.skId, sendBytes, 'OUT')

        except Exception as e:
            self.logger.info(f'SK_ID:{self.skId}- sendToAllChannels Exception :: {e}')



    def threadPoolExcutor(self, instance, msg):
        try:
            start_time = time.time()
            futures = self.executor.submit(instance.run)
            # result = futures.result() #다른 스레드에 영향을 미침
            
            # 운영시 비권장 futures의 블락을 우회하기위해 스레드 선언
            result_thread = threading.Thread(target=self.process_result, args=(futures ,msg, start_time,))
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