from http.server import SimpleHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from xml.dom import NoDataAllowedErr


class HttpServer(ThreadingMixIn,HTTPServer):

    httpThread = None
    initData = None

    def __init__(self, thread, server_address, handler_class):
        super().__init__(server_address, handler_class)
        self.httpThread = thread
        self.initData = thread.initData

