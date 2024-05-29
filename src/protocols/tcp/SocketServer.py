import traceback
from conf.logconfig import logger
import threading
import socket
import socketserver
from src.protocols.tcp.init.ServerInit import ServerInit


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

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

    def run(self):
        self.initServer()

    def initServer(self):
        try:
            self.server = ServerInit(self.initData)
            ip, port = self.server.server_address
            server_thread = threading.Thread(target=self.server.serve_forever)
            server_thread.daemon = True
            server_thread.start()
            logger.info('TCP SERVER Start : SK_ID= {}, IP= {}:{} :: Thread -{}'.format(self.skId, ip, port,server_thread.name))
        except Exception as e:
            logger.info(f'TCP SERVER Bind exception : SK_ID={self.skId}  : {e}' )
            traceback.print_exc()



    def sendAllClient(self):
        self.server.handler.sendAllClient(b'test')




