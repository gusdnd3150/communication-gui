
import socketserver
import traceback
from conf.logconfig import logger
import threading
import queue
from src.protocols.tcp.msg.msg.FreeCodec import FreeCodec

class ServerHandler(socketserver.StreamRequestHandler):

    initData = None
    delimiter = b''

    #############
    skId = ''
    pipeBytes = queue.Queue()
    client_list= []

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
                    codec = FreeCodec(self.initData)

                reableLengthArr = codec.concyctencyCheck(buffer)

                if(len(reableLengthArr) == 0):
                    logger.info('consystency False')
                    continue
                logger.info('consystency True')

                for index, readLegnth in enumerate(reableLengthArr):
                    readByte = buffer[:readLegnth]
                    try:
                        logger.info(f' readLegnth : {readLegnth}')

                        totlaBytes = readByte.copy()
                        data = codec.convertRecieData(readByte)
                        data['TOTAL_BYTES'] = totlaBytes

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
            traceback.print_exc()



    def onReciveData(self, data):
        try:
            logger.info(f'onReciveData bytes :{str(data)}')

            self.sendAllClient(str(data).encode())
        except Exception as e:
            logger.info(f' onReciveData Exception :{e}')