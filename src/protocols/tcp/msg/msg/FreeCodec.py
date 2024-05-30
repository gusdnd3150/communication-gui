import io

from src.protocols.tcp.msg.Decoder import Decoder
import traceback
from conf.logconfig import logger
from conf.InitData_n import socketBody, sokcetIn

class FreeCodec(Decoder):

    initData = None
    hdList = []
    hdId = ''
    hdLen = 0

    delimiter = b''
    hdBytes = bytearray()
    bodyBytes = bytearray()
    
    def __init__(self, initData):
        self.initData= initData
        self.hdId = initData['HD_ID']
        self.hdLen = initData['HD_LEN']

        if initData.get(self.hdId) is not None:
            self.hdList = initData[self.hdId]
        if (initData['SK_DELIMIT_TYPE'] != ''):
            self.delimiter = int(initData['SK_DELIMIT_TYPE'], 16).to_bytes(1, byteorder='big')


    def concyctencyCheck(self,copyBytes):
        result = []
        # 구분자를 통해 패킷을 나누고 패킷별로 읽어들일 개수를 배열로 반환
        try:
            logger.info(self.initData)
            if(self.delimiter != b''):
                messages = copyBytes.split(self.delimiter)
                if len(messages) > 1:
                    for index, msg in enumerate(messages):
                        if(len(msg)>0):
                            result.append(len(msg)+1)
            else:
                result.append(len(copyBytes))

        except Exception as e:
            logger.info(f'concyctencyCheck Exception : {e}')

        return result


    def convertRecieData(self, msgBytes):

        returnData = {}
        mid = None
        msgbody = None

        for index, hd in enumerate(self.hdList):
            read = msgBytes[:hd['DT_LEN']]
            if hd['DT_TYPE'] == 'STRING':
                returnData[hd['DT_ID']] = read.decode('utf-8-sig').strip()
            elif hd['DT_TYPE'] == 'INT':
                returnData[hd['DT_ID']]  = int.from_bytes(read, byteorder='big')
            elif hd['DT_TYPE'] == 'SHORT':
                returnData[hd['DT_ID']]  = int.from_bytes(read, byteorder='big', signed=True)
            elif hd['DT_TYPE'] == 'BYTE' or hd['DT_TYPE'] == 'BYTES':
                returnData[hd['DT_ID']] = read

            del msgBytes[0:hd['DT_LEN']]

        for index, body in enumerate(socketBody):
            if mid == None:
                if (body['MSG_KEY_TYPE'] == 'LENGTH' and body['MSG_LEN'] == len(msgBytes)):
                    msgbody = body
            else:
                if (body['MSG_ID'] == mid):
                    msgbody = body

        logger.info(f'msg body : {str(msgbody)}')


        return returnData

