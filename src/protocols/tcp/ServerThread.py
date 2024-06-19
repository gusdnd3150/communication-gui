import traceback
from conf.logconfig import *
import threading

import socket
from src.protocols.tcp.msg.FreeCodec import FreeCodec
from src.protocols.tcp.msg.LengthCodec import LengthCodec
from conf.InitData_n import systemGlobals

from src.protocols.sch.BzSchedule import BzSchedule
from src.protocols.BzActivator import BzActivator


class ServerThread(threading.Thread):

    initData = None
    skId = ''
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

    def __init__(self, data):
        # {'PKG_ID': 'CORE', 'SK_ID': 'SERVER2', 'SK_GROUP': None, 'USE_YN': 'Y', 'SK_CONN_TYPE': 'SERVER',
        #  'SK_TYPE': 'TCP', 'SK_CLIENT_TYPE': 'KEEP', 'HD_ID': 'HD_FREE', 'SK_PORT': 5556, 'SK_IP': '0.0.0.0',
        #  'SK_DELIMIT_TYPE': '0x00', 'RELATION_VAL': None, 'SK_LOG': 'Y', 'HD_TYPE': 'FREE', 'MSG_CLASS': '',
        #  'MAX_LENGTH': 1024, 'MIN_LENGTH': 4, 'HD_LEN': 0}
        # 'BZ_EVENT_INFO': [{'PKG_ID': 'CORE', 'SK_GROUP': 'TEST', 'BZ_TYPE': 'KEEP', 'USE_YN': 'Y', 'BZ_METHOD': 'TestController.test', 'SEC': 5, 'BZ_DESC': None}]}

        self.initData = data
        self.skId = data['SK_ID']
        self.name = data['SK_ID'] + '-thread'  # 스레드 이름 설정
        self.skIp = data['SK_IP']
        self.skPort = int(data['SK_PORT'])

        self.logger = setup_sk_logger(self.skId)
        self.logger.info(f'SK_ID:{self.skId} - initData : {data}')

        if (self.initData['HD_TYPE'] == 'FREE'):
            self.codec = FreeCodec(self.initData)
        elif (self.initData['HD_TYPE'] == 'LENGTH'):
            self.codec = LengthCodec(self.initData)

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

        super().__init__()

    def run(self):
        self.initServer()


    def initServer(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((self.skIp, self.skPort))
            self.socket.listen(10) #연결수 설정
            self.logger.info(f'TCP SERVER Start : SK_ID= {self.skId}, IP= {self.skIp}:{self.skPort} :: Thread ')
            self.isRun = True

            # 서버 테이블 인설트
            systemGlobals['mainInstance'].addServerRow(self.initData)

            while self.isRun:
                # accept connections from outside
                (clientsocket, address) = self.socket.accept()
                t = threading.Thread(target=self.client_handler, args=(clientsocket, address))
                t.start()
        except Exception as e:
            self.logger.error(f'TCP SERVER Bind exception : SK_ID={self.skId}  : {e}')



    def client_handler(self,clientsocket,  address):
        buffer = bytearray()
        client_info = (self.skId, clientsocket)
        self.logger.info(f' {self.skId} - CLIENT connected  IP/PORT : {address}')


        # ACTIVE 이벤트처리
        if self.bzActive is not None:
            self.logger.info(f'SK_ID:{self.skId} - CHANNEL ACTIVE')
            self.bzActive['SK_ID'] = self.skId
            self.bzActive['CHANNEL'] = clientsocket
            self.bzActive['LOGGER'] = self.logger
            bz = BzActivator(self.bzActive)
            bz.daemon = True
            bz.start()

        # KEEP 처리
        if self.bzKeep is not None:
            self.bzKeep['SK_ID'] = self.skId
            self.bzKeep['CHANNEL'] = clientsocket
            self.bzKeep['LOGGER'] = self.logger
            self.bzSch = BzSchedule(self.bzKeep)
            self.bzSch.daemon = True
            self.bzSch.start()


        # IDLE_READ 처리
        if self.bzIdleRead is not None:
            clientsocket.settimeout(self.bzIdleRead.get('SEC'))

        self.client_list.append(client_info)
        systemGlobals['mainInstance'].modServerRow(self.skId,'CON_COUNT',str(self.countChannelBySkId(self.skId)))

        while self.isRun:
            try:
                reciveBytes = clientsocket.recv(self.initData.get('MAX_LENGTH'))
                if not reciveBytes:
                    break
                buffer.extend(reciveBytes)

                if (self.initData['MIN_LENGTH'] > len(buffer)):
                    continue

                while self.isRun:
                    readBytesCnt = self.codec.concyctencyCheck(buffer.copy())
                    if readBytesCnt == 0:
                        break
                    elif readBytesCnt > len(buffer):
                        break
                    readByte = buffer[:readBytesCnt]
                    try:
                        if self.skLogYn:
                            decimal_string = ' '.join(str(byte) for byte in readByte)
                            self.logger.info(f'SK_ID:{self.skId} read length : {readBytesCnt} decimal_string : [{decimal_string}]')

                        data = self.codec.decodeRecieData(readByte)
                        data['TOTAL_BYTES'] = readByte.copy()
                        data['CHANNEL'] = clientsocket
                        data['SK_ID'] = self.skId
                        data['LOGGER'] = self.logger
                        bz = BzActivator(data)
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
                    self.bzIdleRead['SK_ID'] = self.skId
                    self.bzIdleRead['CHANNEL'] = clientsocket
                    self.bzIdleRead['LOGGER'] = self.logger
                    bz = BzActivator(self.bzIdleRead)
                    bz.daemon = True
                    bz.start()

            # 클라가 연결을 종료할 경우
            except ConnectionResetError as e:
                self.logger.error(f'SK_ID:{self.skId} ConnectionResetError : {e}')
                break
            except Exception as e:
                decimal_string = ' '.join(str(byte) for byte in buffer)
                self.logger.error(f'SK_ID:{self.skId} handler Exception read length : {len(buffer)} decimal_string : [{decimal_string}]')
                self.logger.error(f'SK_ID:{self.skId} handler Exception : {traceback.format_exc()}')
                buffer.clear()

        # 버퍼 클리어
        buffer.clear()
        
        # inactive 처리
        self.logger.info(f'SK_ID:{self.skId}- CLIENT disConnected  IP/PORT : {address}')
        if self.bzInActive is not None:
            self.bzInActive['SK_ID'] = self.skId
            self.bzInActive['CHANNEL'] = clientsocket
            self.bzInActive['LOGGER'] = self.logger
            bz = BzActivator(self.bzInActive)
            bz.daemon = True
            bz.start()

        if self.bzSch is not None:
            self.bzSch.stop()

        self.client_list.remove(client_info)
        self.logger.info(f'SK_ID:{self.skId} remain Clients count({len(self.client_list)})')

        systemGlobals['mainInstance'].modServerRow(self.skId, 'CON_COUNT', str(self.countChannelBySkId(self.skId)))
        clientsocket.close()


    def sendToAllChannels(self, bytes):
        try:
            if len(self.client_list) == 0:
                self.logger.info(f'sendToAllChannels -{self.skIp} has no Clients')
                return
            for skId, client in self.client_list:
                if skId == self.skId:
                    client.sendall(bytes)
        except Exception as e:
            self.logger.info(f'SK_ID:{self.skId}- sendToAllChannels Exception :: {e}')

    def countChannelBySkId(self,skId):
        count = 0
        for skid, socket in self.client_list:
            if skid == skId:
                count += 1
        return count