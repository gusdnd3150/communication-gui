
import socketserver
import traceback
from conf.logconfig import logger
import threading
import queue

class ServerHandler(socketserver.StreamRequestHandler):

    initData = None
    skId = ''
    pipeBytes = queue.Queue()
    client_list= []

    def handle(self):
        try:
            while True:
                cur_thread = threading.current_thread()
                data = self.request.recv(self.initData['MAX_LENGTH']).decode('utf-8')
                if not data:
                    break

                response = bytes("{}: {}".format(cur_thread.name, data), 'ascii')
                print(f'데이터:{data}')
                # self.request.sendall(response)

                self.sendAllClient(response)
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
        logger.info(f" SK_ID:{self.initData['SK_ID']} Close Client : {self.client_address[0]}:{self.client_address[1]}")



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