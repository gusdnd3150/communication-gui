import traceback
from conf.logconfig import logger
import threading
import socket
import socketserver
from src.protocols.tcp.init.ServerInit import ServerInit
from src.utils.Container import Container
from src.protocols.tcp.handler import ServerHandler



class SocketServer(threading.Thread):

    initData = {}
    skId = ''
    skIp = ''
    skPort = 0
    socket = None

    def __init__(self, data):
        # logger.info(data)
        self.initData = data
        self.skId = data['SK_ID']
        self.name = data['SK_ID'] + '-thread'  # 스레드 이름 설정
        self.skIp = data['SK_IP']
        self.skPort = int(data['SK_PORT'])
        super().__init__()

    def run(self):
        self.initServer()

    def initServer(self):
        try:
            self.socket = ServerInit(self.initData)
            ip, port = self.socket.server_address
            server_thread = threading.Thread(target=self.socket.serve_forever)
            server_thread.daemon = True
            server_thread.start()
            logger.info('TCP SERVER Start : SK_ID= {}, IP= {}:{} :: Thread -{}'.format(self.skId, ip, port,server_thread.name))

        except Exception as e:
            # self.server.server_close()
            logger.info(f'TCP SERVER Bind exception : SK_ID={self.skId}  : {e}' )
            traceback.print_exc()



