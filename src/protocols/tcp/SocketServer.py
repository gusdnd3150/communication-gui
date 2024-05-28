
from conf.logconfig import logger
import traceback
from conf.logconfig import logger
import threading
import socket
import select
import io
from src.protocols.tcp.msg.msg.FreeCodec import FreeCodec

class SocketServer(threading.Thread):

    initData = {}
    skId = ''
    skIp = ''
    skPort = 0
    isRun = False
    tryCount = 0

    delimiter = b''
    server = None
    client_list = []
    error_list= []
    maxLen = 0
    minLen = 0
    hdType= ''


    def __init__(self, data):
        logger.info(data)
        self.initData = data
        self.skId = data['SK_ID']
        self.name = data['SK_ID'] + '-thread'  # 스레드 이름 설정
        self.skIp = data['SK_IP']
        self.hdType = data['HD_TYPE']
        self.skPort = int(data['SK_PORT'])
        self.maxLen = int(data['MAX_LENGTH'])
        self.minLen = int(data['MIN_LENGTH'])
        super().__init__()


    def initServer(self):
        logger.info('TCP SERVER Start : SK_ID={}, IP={}, PORT={}'.format(self.skId, self.skIp, self.skPort))
        try:
            self.isRun = True
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind((self.skIp, self.skPort))
            server.listen()
            self.server = server
            self.client_list = [server]
            self.error_list = [server]
            newClient = None
            while self.isRun:
                readables, writeables, excpetions = select.select(self.client_list, [], self.error_list)
                for sock in readables:
                    if sock == server:  # 신규 클라이언트 접속
                        newClient, addr = server.accept()
                        self.client_list.append(newClient)
                        t = threading.Thread(target=self.recive_handler, args=(newClient, addr))
                        t.start()
                for error in excpetions:
                    print(error)
        except:
            logger.info('TCP SERVER Bind exception : SK_ID={}'.format(self.skId))
            # self.isRun = False 서버는 살아있어야함
            traceback.print_stack()


    def recive_handler(self,newClient, addr ):
        logger.info('[Client Connected]::')
        # dataStream = io.BytesIO()
        dataStream = bytearray()
        try:
            while self.isRun:
                data = newClient.recv(self.maxLen)
                if not data:
                    break

                dataStream.extend(data)
                totalByte = len(dataStream)
                msgCodec = None
                if(totalByte > self.minLen):

                    if(self.hdType == 'FREE'):
                        msgCodec = FreeCodec(self.initData)
                    else:
                        break

                    passYn = msgCodec.concyctencyCheck(dataStream.copy())
                    if(passYn == False):
                        logger.info('concyctencyCheck :: False')
                        continue
                    logger.info('concyctencyCheck :: True')

                    msgCodec.setReviceBtyes(dataStream)

                    msgCodec.test()
                        # if self.delimiter != b'':
                #     dataBuf.extend(data)  # 버퍼에 쌓아둠
                #     # messages = dataBuf.split(b"\x00")
                #     messages = dataBuf.split(self.delimiter)
                #     if len(messages) > 1:
                #         for bytes in messages:
                #             if len(bytes) > 0:
                #                 # self.serverReviceMsgMethod(bytes, '{}:{}'.format(addr[0], str(addr[1])))
                #                 logger.info('revice Data : ' + str(bytes))
                #             del dataBuf[0:len(bytes) + 1]
                # else:
                #     logger.info('revice Data : '+ str(data))
        except:
            traceback.print_exc()
            newClient.close()
        finally:
            logger.info('Client Close')

    def run(self):
        self.initServer()


