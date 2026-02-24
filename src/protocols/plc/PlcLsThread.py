import socket
import threading
import time
import traceback
import weakref
from datetime import datetime
from src.protocols.Client import Client
import conf.skModule as moduleData
from conf.logconfig import *
from collections import deque
import queue

class PlcLsThread(threading.Thread, Client):

    initData = None
    socket = None # 소켓
    isRun = False
    isShutdown = False
    plcMaker = None
    commTy = None
    addrAlias = None
    cpuTy = None
    plcIp = None
    plcId = None
    plcPort = None
    client = None
    logYn = None
    plcBuffer = []
    addr_q = deque()
    write_q = queue.Queue(maxsize=20)

    def __init__(self, data):
        self.initData = data
        self.plcId = data['PLC_ID']
        self.plcIp = data['PLC_IP']
        self.plcPort = int(data['PLC_PORT'])
        self.cpuTy = data['CPU_TY']
        self.slot = int(data['SLOT'])
        self.rack = int(data['RACK'])

        if len(data.get('ADDR_LIST')) > 0:
            for addr in data.get('ADDR_LIST'):
                self.plcBuffer.append({"addr": addr['ADDR'],"pos": addr['POS'],"length": addr['LENGTH'],"alias": addr['ADDR_ALIAS'],"data": bytearray()})
                self.addr_q.append((addr['ADDR'], addr['POS'], addr['LENGTH'], addr['ADDR_ALIAS']))

        self.commTy = data.get('COMM_TY', 'binary')
        self.logYn = True if data.get('LOG_YN','N') == 'Y' else False

        self.pending = None  # 현재 요청중인 addr tuple
        self.pending_sent_at = 0.0  # 요청 전송 시각
        self.pending_timeout = 3.0  # 응답 대기 제한(초) - 환경에 맞게
        self.lock = threading.Lock()

        # write pending 따로 (read pending 건드리지 않음)
        self.write_pending = None
        self.write_sent_at = 0.0
        self.write_timeout = 3.0

        super(PlcLsThread, self).__init__()
        self._stop_event = threading.Event()

    def __del__(self):
        logger.info(f'Thread {self.plcId} is deleted')

    def run(self):
        # moduleData.mainInstance.addClientRow(self.initData)
        self.initClient()

    def stop(self):
        try:
            self.isRun = False
            self.isShutdown = True
            if self.client:
                self.client.close()
        except Exception as e:
            self.logger.error(f'PLC_ID:{self.plcId} Stop fail : {traceback.format_exc()}')
        finally:
            self._stop_event.set()

            # moduleData.mainInstance.deleteTableRow(self.plcId, 'list_run_client')

    def initClient(self):

        while not self.isShutdown:
            conn_list = None
            channelInfo = None

            try:
                # 서버에 연결합니다.
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((self.plcIp, int(self.plcPort)))
                self.socket.settimeout(2)

                logger.info('PLC CLIENT Start : PLC_ID={}, IP={}, PORT={}'.format(self.plcId, self.plcIp, self.plcPort))
                channelInfo = {
                    'PLC_ID': self.plcId
                    , 'SK_GROUP': ''
                    , 'CHANNEL': self.socket
                    , 'THREAD': weakref.ref(self)
                }
                conn_list = (self.plcId, self.socket, weakref.ref(self))
                moduleData.runChannels.append(conn_list)  # 참조
                moduleData.mainInstance.updateConnList()

                self.isRun = True
                self.send_next_request()

                with self.socket:
                    while self.socket:
                        try:
                            reciveBytes = self.socket.recv(9999)
                            try:
                                if self.logYn:
                                    decimal_string = ' '.join(str(byte) for byte in reciveBytes)
                                    logger.info(
                                        f'PLC_ID:{self.plcId} recive_string:[{reciveBytes.decode("utf-8", errors="replace")}] decimal_string : [{decimal_string}] read length : {len(reciveBytes)} ')

                                self.on_response(reciveBytes)
                            except Exception as e:
                                logger.error(f'PLC_ID:{self.plcId} Message parsing Exception : buffer= {str(reciveBytes)} {e}')

                        except socket.timeout:
                            logger.info(f'{self.plcId} : [IDLE CHANNEL CLOSE]')
                            self.pending = None
                            self.socket.close()
                            break
                        except Exception as e:
                            logger.error(f'PLC_ID={self.plcId} connection exception : {traceback.format_exc()}')
                            self.isRun = False
                            break
            except Exception as e:
                self.isRun = False
                logger.error(f'PLC_ID={self.plcId}  TCP CLIENT try to connect exception : {e}')
            finally:
                if conn_list in moduleData.runChannels:
                    moduleData.runChannels.remove(conn_list)
                moduleData.mainInstance.updateConnList()

                if self.socket:
                    self.socket.close()
                    self.socket = None

                if self.isShutdown == False:
                    conn_list = None
                    channelInfo = None
                    self.socket = None
                    time.sleep(5)  # 5초 대기 후 재시도


    def threadPoolExcutor(self, instance):
        try:
            futures = self.executor.submit(instance.run)
            # result = futures.result() #다른 스레드에 영향을 미침
        except:
            self.logger.info(f'threadPoolExcutor exception : PLC_ID:{self.plcId} - {traceback.format_exc()}')

    def process_result(self, future, msg, start_time):
        try:
            result = future.result()
            # 결과를 처리하는 로직
            if self.logYn:
                end_time = time.time()
                start = datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')
                end = datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')
                # logger.info(f"----------- PLC_ID: {self.plcId} future Result: {result} and remain thread Que : {self.executor._work_queue}")
                self.logger.info(
                    f'----------- PLC_ID: {self.plcId} - {msg} begin:{start} end:{end} total time: {round(end_time - start_time, 4)}------------')
        except Exception as e:
            self.logger(f"Exception while processing result: {e}")

    def send_next_request(self):
        """pending이 없을 때만 다음 주소 요청을 보냄"""
        with self.lock:
            if not self.socket or self.pending is not None:
                return

            # ✅ write가 있으면 write 먼저 보냄 (read 구조는 그대로)
            if self.write_pending is None:
                try:
                    self.write_pending = self.write_q.get_nowait()
                    self.write_sent_at = time.time()
                except queue.Empty:
                    self.write_pending = None

        # lock 밖에서 send
        if self.write_pending is not None:
            try:
                self.send_write_request(self.write_pending)
                # write는 “응답이 오면 완료 처리”하려면 on_response에서 판단해야 함
                # 일단은 "전송 완료 후 바로 버림" 모드면 여기서 버려도 됨 (응답 확인 안 함)
                with self.lock:
                    self.write_pending = None
            except Exception:
                logger.error(f'PLC_ID:{self.plcId} send_write_request fail: {traceback.format_exc()}')
                with self.lock:
                    self.write_pending = None
            # write 처리했으면 read는 다음 사이클(다음 응답/루프)에서
            return

        # ---- 여기부터는 기존 read 로직 그대로 ----
        with self.lock:
            if not self.addr_q:
                return
            addr_tuple = self.addr_q[0]
            self.pending = addr_tuple
            self.pending_sent_at = time.time()

        self.send_read_request(addr_tuple)

    def send_read_request(self, addr_tuple):
        addr, pos, length, alias = addr_tuple

        # TODO: 여기서 LS PLC 프로토콜에 맞는 READ frame 만들기
        # 예시로 dict 만들고 -> codec encode -> bytes
        sendObj = {
            "MSG_ID": "READ",
            "ADDR": addr,
            "POS": pos,
            "LENGTH": length,
            "ALIAS": alias,
        }

        # 지금은 테스트 바이트
        sendBytes = b"test"
        try:
            self.socket.sendall(sendBytes)
            if self.logYn:
                decimal_string = ' '.join(str(b) for b in sendBytes)
                logger.info(f'PLC_ID:{self.plcId} TX addr={addr} len={len(sendBytes)} dec=[{decimal_string}]')
        except Exception:
            logger.error(f'PLC_ID:{self.plcId} send_read_request fail: {traceback.format_exc()}')
            # 전송 실패면 pending 초기화하고 재연결 루프로
            with self.lock:
                self.pending = None
            try:
                self.socket.close()
            except:
                pass

    def on_response(self, reciveBytes: bytes):
        """
        응답 파싱 성공 시:
        - pending 주소의 last_bytes 업데이트
        - addr_q를 라운드로빈 회전
        - pending 비우고 다음 요청 보내기
        """
        # TODO: reciveBytes를 실제로 파싱해서 "어떤 주소의 응답인지" 확인 가능하면 더 안전함
        # 일단은 'pending 요청의 응답'으로 간주
        with self.lock:
            if self.pending is None:
                return
            addr, pos, length, alias = self.pending
            # last_bytes 저장(원하는 형태로 변환/저장)
            new_tuple = (addr, pos, length, alias)

            for item in self.plcBuffer:
                if item["addr"] == addr:
                    item["data"] = bytearray(reciveBytes)

            # 라운드로빈: 맨 앞을 빼서 맨 뒤로
            self.addr_q.popleft()
            self.addr_q.append(new_tuple)

            self.pending = None
        # 다음 요청 바로 보냄
        self.send_next_request()


    def sendBytesToChannel(self, channel, bytes):
        pass

    def sendBytesToAllChannels(self, bytes):
        pass

    def sendMsgToAllChannels(self, obj):
        try:
            if self.socket:
                sendBytes = b'test'
                self.socket.sendall(sendBytes)
                if self.logYn:
                    decimal_string = ' '.join(str(byte) for byte in sendBytes)
                    logger.info(
                        f'PLC_ID:{self.plcId} send bytes length : {len(sendBytes)} send_string:[{sendBytes.decode("utf-8", errors="replace")}] decimal_string : [{decimal_string}]')
                    # moduleData.mainInstance.insertLog(self.plcId, sendBytes, 'OUT')
            else:
                logger.info(f'PLC_ID:{self.plcId}- sendMsgToAllChannels has no connection')
        except Exception as e:
            logger.info(f'PLC_ID:{self.plcId}- sendMsgToAllChannels Exception :: {e}')

    def sendMsgToChannel(self, channel, obj):
        pass

    def enqueue_write(self, addr: str, value_bytes: bytes, pos=0, length=None, alias=""):
        if length is None:
            length = len(value_bytes)
        req = {
            "ADDR": addr,
            "POS": pos,
            "LENGTH": length,
            "ALIAS": alias,
            "VALUE": value_bytes,
        }
        try:
            self.write_q.put_nowait(req)
        except queue.Full:
            logger.warning(f"PLC_ID:{self.plcId} write_q FULL -> drop addr={addr}")

    def send_write_request(self, req: dict):
        addr = req["ADDR"]
        value_bytes = req["VALUE"]

        # TODO: FEnet WRITE frame로 교체
        sendBytes = b"test"  # <-- 여기에 value 포함한 실제 프레임 만들기

        self.socket.sendall(sendBytes)
        if self.logYn:
            decimal_string = ' '.join(str(b) for b in sendBytes)
            logger.info(f'PLC_ID:{self.plcId} TX(WRITE) addr={addr} len={len(sendBytes)} dec=[{decimal_string}]')
