
import socketserver
import traceback
from conf.logconfig import logger
import threading
import queue
from src.protocols.tcp.msg.FreeCodec import FreeCodec
from src.protocols.tcp.msg.LengthCodec import LengthCodec

from conf.InitData_n import systemGlobals



class ServerHandler(socketserver.StreamRequestHandler):

    initData = None
    delimiter = b''

    #############
    skId = ''
    pipeBytes = queue.Queue()
    client_list = []

    def handle(self):
        try:

            if (self.initData['SK_DELIMIT_TYPE'] != ''):
                self.delimiter = int(self.initData['SK_DELIMIT_TYPE'], 16).to_bytes(1, byteorder='big')
            buffer = bytearray()
            while True:
                cur_thread = threading.current_thread()
                reciveBytes = self.request.recv(self.initData['MAX_LENGTH'])
                if not reciveBytes:
                    break
                buffer.extend(reciveBytes)

                # 최소길이 확보
                if (self.initData['MIN_LENGTH'] > len(buffer)):
                    continue

                codec = None
                if (self.initData['HD_TYPE'] == 'FREE'):
                    codec = FreeCodec(self.initData)

                elif (self.initData['HD_TYPE'] == 'LENGTH'):
                    codec = LengthCodec(self.initData)

                reableLengthArr = codec.concyctencyCheck(buffer)

                if(len(reableLengthArr) == 0):
                    logger.info('consystency False')
                    continue
                logger.info('consystency True')

                for index, readLegnth in enumerate(reableLengthArr):
                    readByte = buffer[:readLegnth]
                    try:
                        totlaBytes = readByte.copy()
                        data = codec.decodeRecieData(readByte)
                        data['TOTAL_BYTES'] = totlaBytes
                        data['CHANNEL'] = self.request

                        reciveThread = threading.Thread(target=self.onReciveData, args=(data,))
                        reciveThread.daemon = True
                        reciveThread.start()

                    except Exception as e:
                        logger.info(f' Msg convert Exception : {e}  {str(buffer)}')
                    finally:
                        del buffer[0:readLegnth]


        except TimeoutError:
            logger.info(f"SK_ID:{self.initData['SK_ID']} Client IDLE READ: {self.client_address[0]}:{self.client_address[1]}")
            self.handle()
        except Exception as e:
            logger.info(f" SK_ID:{self.initData['SK_ID']} Client dis Connected: {self.client_address[0]}:{self.client_address[1]} exception : {e}")

    def setup(self):
        super().setup()
        # 클라이언트 접속 감지
        self.client_list.append(self.request)
        bzList = self.initData['BZ_EVENT_INFO']
        logger.info('setup 클라이언트 접속 이벤트')
        for index, bzData in enumerate(bzList):
            if bzData['BZ_TYPE'] is not None:
                bzData['CHANNEL'] = self.request
                bzEventThread = threading.Thread(target=self.setBzEvent, args=(bzData,))
                bzEventThread.daemon = True
                bzEventThread.start()


        logger.info(f" SK_ID:{self.initData['SK_ID']} Client connected: {self.client_address[0]}:{self.client_address[1]}")


    def finish(self):
        self.client_list.remove(self.request)
        logger.info(f" SK_ID:{self.initData['SK_ID']} Close Client : {self.client_address[0]}:{self.client_address[1]} and client_list size : {len(self.client_list)}")



    def sendAllClient(self, msgByte):
        try:
            if(len(self.client_list) == 0):
                logger.error(f" SK_ID:{self.initData['SK_ID']} has no Clients")
                return

            for sock in self.client_list:
                try:
                    sock.sendall(msgByte)
                except Exception as e:
                    logger.error(f"Error sending message to {sock.getpeername()}: {e}")
        except:
            traceback.logger.info_exc()

    def sendAllObjectDataClient(self, objData):
        try:
            codec = None
            if (self.initData['HD_TYPE'] == 'FREE'):
                codec = FreeCodec(self.initData)

            self.sendAllBytes(self, codec.encodeSendData(objData))
        except Exception as e:
            logger.info(f'ServerHandler sendAllObjectDataClient() Exception :: {e}')

    def onReciveData(self, data):
        try:
            logger.info('onReciveData')
            logger.info(data)
            if(data.get('IN_MSG_INFO') is not None):
                if(data.get('IN_MSG_INFO').get('BZ_METHOD') is not None):
                    bzClass = data.get('IN_MSG_INFO').get('BZ_METHOD')
                    classNm = bzClass.split('.')[0]
                    methdNm = bzClass.split('.')[1]
                    if classNm in systemGlobals:
                        my_class = systemGlobals[classNm]
                        method = getattr(my_class, methdNm)
                        if callable(method):
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


    def setBzEvent(self, data):
        try:
            # ACTIVE, INAVTIVE, KEEP
            bzType = data['BZ_TYPE']
            # {'PKG_ID': 'CORE', 'SK_GROUP': 'TEST', 'BZ_TYPE': 'ACTIVE', 'USE_YN': 'Y', 'BZ_METHOD': 'TestController.test', 'SEC': None, 'BZ_DESC': None, 'CHANNEL':''}
            if(data.get('BZ_METHOD') is not None):
                bzClass = data.get('BZ_METHOD')
                classNm = bzClass.split('.')[0]
                methdNm = bzClass.split('.')[1]
                if classNm in systemGlobals:
                    my_class = systemGlobals[classNm]
                    method = getattr(my_class, methdNm)
                    if callable(method):
                        method(data)
                    else:
                        raise Exception(f"setBzEvent :{methdNm} is not callable.")
                else:
                    raise Exception(f"Class {classNm} not found.")
            else:
                raise Exception(f'BZ_METHOD is Null :')

        except Exception as e:
            # traceback.logger.info_exc()
            logger.info(f'ServerHandler setBzEvent() Exception :{e}')



    def sendAllBytes(self, msgBytes):
        for sock in self.client_list:
            try:
                sock.sendall(msgBytes)
            except Exception as e:
                logger.error(f"ServerHandler sendAllBytes() Exception :: {sock.getpeername()}: {e}")
