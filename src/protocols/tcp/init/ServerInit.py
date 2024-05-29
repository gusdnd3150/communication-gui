
from conf.logconfig import logger
import traceback
import socketserver
from src.protocols.tcp.handler.ServerHandler import ServerHandler

class ServerInit(socketserver.ThreadingMixIn, socketserver.TCPServer):

    initData = None
    handler = None

    def __init__(self, iniData):
        self.initData = iniData
        self.daemon_threads = True
        ServerHandler.timeout = 5 #idle
        ServerHandler.initData = iniData
        self.handler = ServerHandler
        super().__init__((iniData['SK_IP'], int(iniData['SK_PORT'])), self.handler)

    def finish_request(self, request, client_address):
        self.RequestHandlerClass(request, client_address, self)