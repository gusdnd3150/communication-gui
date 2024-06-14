import traceback
from conf.logconfig import logger
import threading

import socket
from src.protocols.tcp.msg.FreeCodec import FreeCodec
from conf.InitData_n import systemGlobals

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

    def __init__(self, data):
        # {'PKG_ID': 'CORE', 'SK_ID': 'SERVER2', 'SK_GROUP': None, 'USE_YN': 'Y', 'SK_CONN_TYPE': 'SERVER',
        #  'SK_TYPE': 'TCP', 'SK_CLIENT_TYPE': 'KEEP', 'HD_ID': 'HD_FREE', 'SK_PORT': 5556, 'SK_IP': '0.0.0.0',
        #  'SK_DELIMIT_TYPE': '0x00', 'RELATION_VAL': None, 'SK_LOG': 'Y', 'HD_TYPE': 'FREE', 'MSG_CLASS': '',
        #  'MAX_LENGTH': 1024, 'MIN_LENGTH': 4, 'HD_LEN': 0}

        logger.info(f' ServerThread initData : {data}')
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
        super().__init__()

    def run(self):
        self.initServer()


    def initServer(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((self.skIp, self.skPort))
            self.socket.listen(5) #연결수 설정
            logger.info('TCP SERVER Start : SK_ID= {}, IP= {}:{} :: Thread '.format(self.skId, self.skIp, self.skPort))
            self.isRun = True
            while self.isRun:
                # accept connections from outside
                (clientsocket, address) = self.socket.accept()
                t = threading.Thread(target=self.client_handler, args=(clientsocket, address))
                t.start()
        except Exception as e:
            logger.info(f'TCP SERVER Bind exception : SK_ID={self.skId}  : {e}' )



    def client_handler(self,clientsocket,  address):
        buffer = bytearray()
        # avtive 이벤트처리
        logger.info(f' {self.skId} - Client connected  IP/PORT : {address}')

        # idle 처리
        # clientsocket.settimeout(5)
        client_info = (self.skId, clientsocket)

        self.client_list.append(client_info)
        while self.isRun:
            try:
                reciveBytes = clientsocket.recv(self.initData.get('MAX_LENGTH'))
                if not reciveBytes:
                    break
                buffer.extend(reciveBytes)
                logger.info(f'{self.skId} recieved data: {reciveBytes}')

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

                        reciveThread = threading.Thread(target=self.onReciveData, args=(data,))
                        reciveThread.daemon = True
                        reciveThread.start()
                    except Exception as e:
                        logger.info(f'SK_ID:{self.skId} Msg convert Exception : {e}  {str(buffer)}')
                    finally:
                        del buffer[0:readLegnth]

            except socket.timeout as e:
                logger.info(f'{self.skId}- Timeout IDLE read : {e}')

            # 클라가 연결을 종료할 경우
            except ConnectionResetError as e:
                logger.info(f'ConnectionResetError : {e}')
                break

            except Exception as e:
                logger.info(f'handler Exception : {e}')
                break


        # 버퍼 클리어
        buffer.clear()
        
        # inactive 처리
        logger.info(f' {self.skId} - Client disConnected  IP/PORT : {address}')

        self.client_list.remove(client_info)
        logger.info(f' {len(self.client_list)}')
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
            logger.info(f'{self.skIp}- sendToAllChannels Exception : data STR [{str(bytes)}]  error [{e}]')

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
                            logger.info(f"onReciveData : {classNm}.{methdNm} call.")
                            method(data)
                        else:
                            logger.info(f"{methdNm} is not callable.")
                    else:
                        logger.info(f"Class {classNm} not found.")
                else:
                    logger.info(f'BZ_METHOD INFO is Null :')
                    return
            else:
                logger.info(f'IN_MSG_INFO INFO is Null :')
                return

        except Exception as e:
            traceback.logger.info_exc()
            logger.info(f'ServerHandler onReciveData() Exception :{e}')