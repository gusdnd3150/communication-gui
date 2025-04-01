
from http.server import BaseHTTPRequestHandler
from conf.logconfig import *

class HttpRequestHandler(BaseHTTPRequestHandler):


    def do_GET(self):
        server_instance = self.server
        logger = server_instance.httpThread.logger # HttpServer 의 인스턴스
        # logger.info(server_instance.httpThread)
        logger.info(f'sss')

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<h1>Hello, World!</h1>")

    def do_POST(self):
        server_instance = self.server
        logger = server_instance.httpThread.logger  # HttpServer 의 인스턴스

        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)  # 바디 데이터 읽기
        print(f"Received POST data: {post_data.decode()}")

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"POST request received")


    def send(self, msg):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<h1>Hello, World!</h1>")