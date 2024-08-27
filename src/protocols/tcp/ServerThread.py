import traceback
from conf.logconfig import *
import threading

import socket
from src.protocols.msg.FreeCodec import FreeCodec
from src.protocols.msg.LengthCodec import LengthCodec
from src.protocols.msg.JSONCodec import JSONCodec
from conf.skModule import systemGlobals
import conf.skModule as moduleData

from src.protocols.sch.BzSchedule import BzSchedule
from src.protocols.sch.BzSchedule2 import BzSchedule2
from src.protocols.BzActivator import BzActivator
from src.protocols.Server import Server

class ServerThread(threading.Thread, Server):

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
    client_list = []
    bzKeep = None
    bzActive = None
    bzInActive = None
    bzIdleRead = None
    bzSchList = []
    logger = None
    clientThreads = []

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

        super(ServerThread,self).__init__()
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

            if len(self.client_list) > 0:
                for skId, client, codec in self.client_list:
                    try:
                        client.close()
                    except:
                        self.logger.error(f'SK_ID:{self.skId} disConnected Client : {client}')

            if len(self.bzSchList) > 0:
                for item in self.bzSchList:
                    item.stop()
                    item.join()
            self.socket.close()
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
                    # accept connections from outside
                    (clientsocket, address) = self.socket.accept()
                    t = threading.Thread(target=self.client_handler, args=(clientsocket, address))
                    t.daemon = True
                    t.start()
                    self.clientThreads.append(t)
        except Exception as e:
            self.logger.error(f'TCP SERVER Bind exception : SK_ID={self.skId}  : {e}')
        finally:
            self.socket.close()



    def client_handler(self,clientsocket,  address):
        buffer = bytearray()
        client_info = (self.skId, clientsocket, self.codec)
        self.client_list.append(client_info)
        bzSch = None
        chinfo = {
            'SK_ID': self.skId
            ,'SK_GROUP': self.skGrp
            , 'CHANNEL': clientsocket
            , 'CODEC': self.codec
            , 'LOGGER': self.logger
        }
        self.logger.info(f' {self.skId} - CLIENT connected  IP/PORT : {address}')

        connInfo = {}
        connInfo['SK_ID'] = self.skId
        connInfo['CONN_INFO'] = address
        moduleData.mainInstance.addConnRow(connInfo)
        moduleData.runChannels.append(client_info)
        moduleData.mainInstance.modServerRow(self.skId, 'CON_COUNT', str(self.countChannelBySkId(self.skId)))

        try:
            # ACTIVE 이벤트처리
            if self.bzActive is not None:
                self.logger.info(f'SK_ID:{self.skId} - CHANNEL ACTIVE')
                combined_dict = {**chinfo, **self.bzActive}
                bz = BzActivator(combined_dict)
                bz.daemon = True
                bz.start()

            # KEEP 처리
            if self.bzKeep is not None:
                combined_dict = {**chinfo, **self.bzKeep}
                bzSch = BzSchedule(combined_dict)
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

                                copybytes = readByte.copy()
                                data = self.codec.decodeRecieData(readByte)
                                data['TOTAL_BYTES'] = copybytes

                                reciveObj = {**chinfo, **data}
                                bz = BzActivator(reciveObj)
                                bz.daemon = True
                                bz.start()
                            except Exception as e:
                                traceback.print_exc()
                                self.logger.error(f'SK_ID:{self.skId} Msg convert Exception : {e}  {str(buffer)}')
                            finally:
                                del buffer[0:readBytesCnt]

                    except socket.timeout as e:
                        self.logger.error(f'SK_ID:{self.skId}- IDLE READ exception : {e}')
                        if self.bzIdleRead is not None:
                            combined_dict = {**chinfo, **self.bzIdleRead}
                            bz = BzActivator(combined_dict)
                            bz.daemon = True
                            bz.start()

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
                combined_dict = {**chinfo, **self.bzInActive}
                bz = BzActivator(combined_dict)
                bz.daemon = True
                bz.start()

            if bzSch is not None:
                bzSch.stop()
                bzSch.join()

            # self.bzSchList.remove(bzSch)
            if bzSch in self.bzSchList:
                self.bzSchList.remove(bzSch)

            moduleData.mainInstance.deleteTableRow(str(address),'list_conn')

            if clientsocket:
                if client_info in self.client_list:
                    self.client_list.remove(client_info)
                if client_info in moduleData.runChannels:
                    moduleData.runChannels.remove(client_info)

                self.logger.info(f'moduleData.runChannels : {moduleData.runChannels}')
                self.logger.info(f'SK_ID:{self.skId} remain Clients count {len(self.client_list)})')
                moduleData.mainInstance.modServerRow(self.skId, 'CON_COUNT', str(self.countChannelBySkId(self.skId)))
                clientsocket.close()
        except:

            self.logger.error(f'SK_ID:{self.skId} excepton : {traceback.format_exc()}')
            if clientsocket:
                clientsocket.close()

        finally:
                if client_info in self.client_list:
                    self.client_list.remove(client_info)
                if client_info in moduleData.runChannels:
                    moduleData.runChannels.remove(client_info)
                moduleData.mainInstance.modServerRow(self.skId, 'CON_COUNT', str(self.countChannelBySkId(self.skId)))

    def countChannelBySkId(self,skId):
        count = 0
        for skid, socket, codec in self.client_list:
            if skid == skId:
                count += 1
        return count

    def sendBytesToAllChannels(self, bytes):
        try:
            if len(self.client_list) == 0:
                self.logger.info(f'sendToAllChannels -{self.skId} has no Clients')
                return
            for skId, client, codec in self.client_list:
                if skId == self.skId:
                    client.sendall(bytes)
                    if self.skLogYn:
                        decimal_string = ' '.join(str(byte) for byte in bytes)
                        self.logger.info(f'SK_ID:{self.skId} send bytes length : {len(bytes)} send_string:[{str(bytes)}] decimal_string : [{decimal_string}]')

        except Exception as e:
            self.logger.info(f'SK_ID:{self.skId}- sendToAllChannels Exception :: {e}')


    def sendBytesToChannel(self,channel, bytes):
        try:
            if self.skLogYn:
                decimal_string = ' '.join(str(byte) for byte in bytes)
                self.logger.info(f'SK_ID:{self.skId} send bytes length : {len(bytes)} send_string:[{str(bytes)}] decimal_string : [{decimal_string}]')
            channel.sendall(bytes)
        except:
            self.logger.error(f'SK_ID:{self.skId}- sendMsgToChannel Exception :: {traceback.format_exc()}')



    def sendMsgToAllChannels(self, obj):

        try:
            if len(self.client_list) == 0:
                self.logger.info(f'sendToAllChannels -{self.skId} has no Clients')
                return
            sendBytes = self.codec.encodeSendData(obj)

            for skId, client, codec in self.client_list:
                if skId == self.skId:
                    client.sendall(sendBytes)
                    if self.skLogYn:
                        decimal_string = ' '.join(str(byte) for byte in sendBytes)
                        self.logger.info(
                            f'SK_ID:{self.skId} send bytes length : {len(sendBytes)} send_string:[{str(sendBytes)}] decimal_string : [{decimal_string}]')

        except Exception as e:
            self.logger.info(f'SK_ID:{self.skId}- sendToAllChannels Exception :: {e}')

    def sendMsgToChannel(self, channel, obj):

        try:
            if len(self.client_list) == 0:
                self.logger.info(f'sendToAllChannels -{self.skId} has no Clients')
                return
            sendBytes = self.codec.encodeSendData(obj)
            if self.skLogYn:
                decimal_string = ' '.join(str(byte) for byte in sendBytes)
                self.logger.info(f'SK_ID:{self.skId} send bytes length : {len(sendBytes)} send_string:[{str(sendBytes)}] decimal_string : [{decimal_string}]')
            channel.sendall(sendBytes)
        except Exception as e:
            self.logger.info(f'SK_ID:{self.skId}- sendToAllChannels Exception :: {e}')

