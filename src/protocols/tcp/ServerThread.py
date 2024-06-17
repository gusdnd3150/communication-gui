import traceback
from conf.logconfig import logger
import threading

import socket
from src.protocols.tcp.msg.FreeCodec import FreeCodec
from conf.InitData_n import systemGlobals

systemGlobals['mainLayout']

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

        if (self.initData['HD_TYPE'] == 'FREE'):
            self.codec = FreeCodec(self.initData)

        if (data.get('SK_LOG') is not None and data.get('SK_LOG') == 'Y'):
            self.skLogYn = True

        if (self.initData['SK_DELIMIT_TYPE'] != ''):
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
            logger.info('TCP SERVER Start : SK_ID= {}, IP= {}:{} :: Thread '.format(self.skId, self.skIp, self.skPort))
            self.isRun = True
            while self.isRun:
                # accept connections from outside
                (clientsocket, address) = self.socket.accept()
                t = threading.Thread(target=self.client_handler, args=(clientsocket, address))
                t.start()
        except Exception as e:
            logger.error(f'TCP SERVER Bind exception : SK_ID={self.skId}  : {e}' )



    def client_handler(self,clientsocket,  address):
        buffer = bytearray()
        client_info = (self.skId, clientsocket)
        logger.info(f' {self.skId} - CLIENT connected  IP/PORT : {address}')

        # ACTIVE 이벤트처리
        if self.bzActive is not None:
            logger.info(f'SK_ID:{self.skId} - CHANNEL ACTIVE')
            activeObj = {}
            activeObj['CHANNEL'] = clientsocket
            activeObj['IN_MSG_INFO'] = self.bzActive
            reciveThread = threading.Thread(target=self.onReciveData, args=(activeObj,))
            reciveThread.daemon = True
            reciveThread.start()

        # IDLE_READ 처리
        if self.bzIdleRead is not None:
            clientsocket.settimeout(self.bzIdleRead.get('SEC'))


        self.client_list.append(client_info)
        while self.isRun:
            try:
                reciveBytes = clientsocket.recv(self.initData.get('MAX_LENGTH'))
                if not reciveBytes:
                    break
                buffer.extend(reciveBytes)
                logger.info(f'SK_ID:{self.skId} recieved data: {reciveBytes}')

                if (self.initData['MIN_LENGTH'] > len(buffer)):
                    continue

                reableLengthArr = self.codec.concyctencyCheck(buffer)

                if (len(reableLengthArr) == 0):
                    logger.info(f'SK_ID: {self.skId} consystency False {str(buffer)}')
                    continue
                logger.info(f'SK_ID: {self.skId} consystency True ')


                for index, readLegnth in enumerate(reableLengthArr):
                    readByte = buffer[:readLegnth]
                    try:
                        totlaBytes = readByte.copy()
                        data = self.codec.decodeRecieData(readByte)
                        data['TOTAL_BYTES'] = totlaBytes
                        data['CHANNEL'] = clientsocket
                        data['SK_ID'] = self.skId
                        data['SK_ID'] = self.skId

                        reciveThread = threading.Thread(target=self.onReciveData, args=(data,))
                        reciveThread.daemon = True
                        reciveThread.start()
                    except Exception as e:
                        logger.error(f'SK_ID:{self.skId} Msg convert Exception : {e}  {str(buffer)}')
                    finally:
                        del buffer[0:readLegnth]

            except socket.timeout as e:
                logger.error(f'{self.skId}- Timeout IDLE read : {e}')
                if self.bzIdleRead is not None:
                    idleObj = {}
                    idleObj['CHANNEL'] = clientsocket
                    idleObj['IN_MSG_INFO'] = self.bzIdleRead
                    reciveThread = threading.Thread(target=self.onReciveData, args=(idleObj,))
                    reciveThread.daemon = True
                    reciveThread.start()

            # 클라가 연결을 종료할 경우
            except ConnectionResetError as e:
                logger.error(f'SK_ID:{self.skId} ConnectionResetError : {e}')
                break

            except Exception as e:
                logger.error(f'SK_ID:{self.skId} handler Exception : {e}')
                break


        # 버퍼 클리어
        buffer.clear()
        
        # inactive 처리
        logger.info(f'SK_ID:{self.skId}- CLIENT disConnected  IP/PORT : {address}')
        if self.bzInActive is not None:
            inactiveObj = {}
            inactiveObj['CHANNEL'] = clientsocket
            inactiveObj['IN_MSG_INFO'] = self.bzInActive
            reciveThread = threading.Thread(target=self.onReciveData, args=(inactiveObj,))
            reciveThread.daemon = True
            reciveThread.start()

        self.client_list.remove(client_info)
        logger.info(f'SK_ID:{self.skId} remain Clients count({len(self.client_list)})')
        clientsocket.close()


    def sendToAllChannels(self, bytes):
        try:

            if len(self.client_list) == 0:
                logger.info(f'sendToAllChannels -{self.skIp} has no Clients')
                return
            for skId, client in self.client_list:
                if skId == self.skId:
                    client.sendall(bytes)
        except Exception as e:
            logger.info(f'SK_ID:{self.skId}- sendToAllChannels Exception :: {e}')

    def onReciveData(self, data):
        try:
            # logger.info('onReciveData')
            if (data.get('IN_MSG_INFO') is not None):
                if (data.get('IN_MSG_INFO').get('BZ_METHOD') is not None):
                    bzClass = data.get('IN_MSG_INFO').get('BZ_METHOD')
                    classNm = bzClass.split('.')[0]
                    methdNm = bzClass.split('.')[1]
                    if classNm in systemGlobals:
                        my_class = systemGlobals[classNm]
                        method = getattr(my_class, methdNm)
                        if callable(method):
                            logger.info(f"SK_ID:{self.skId} onReciveData : {classNm}.{methdNm} call.")
                            method(data)
                        else:
                            logger.error(f"SK_ID:{self.skId} {methdNm} is not callable.")
                    else:
                        logger.error(f"SK_ID:{self.skId} Class {classNm} not found.")
                else:
                    logger.error(f'SK_ID:{self.skId} BZ_METHOD INFO is Null :')
                    return
            else:
                logger.error(f'SK_ID:{self.skId} IN_MSG_INFO INFO is Null :')
                return

        except Exception as e:
            logger.error(f'SK_ID:{self.skId} ServerHandler onReciveData() Exception :{e}')
            traceback.logger.info_exc()
