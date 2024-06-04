import io

from src.protocols.tcp.msg.Decoder import Decoder
import traceback
from conf.logconfig import logger
from conf.InitData_n import systemGlobals


from src.utils.Utilitys import *


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
            logger.info(f'FreeCodec concyctencyCheck Exception : {e}')

        return result


    def convertRecieData(self, msgBytes):
        returnData = {}
        msgInfo = None

        inMsgVal = None
        msgLen = len(msgBytes)

        inMsgId = None
        bodyList = None

        for index, hd in enumerate(self.hdList):
            if (len(msgBytes) < hd['DT_LEN']):
                raise Exception('FreeCodec convertRecieData : 해더 전문 파싱 오류')
            read = msgBytes[:hd['DT_LEN']]
            returnData[hd['DT_ID']] = decodeBytesToType(read, hd['DT_TYPE'])
            # FREE형은 길이로 나누지 않음
            # if hd.get('MSG_LEN_REL_YN') is not None and hd.get('MSG_LEN_REL_YN') == 'Y':
            #     lenRelYn = returnData[hd['DT_ID']]
            if hd.get('MSG_ID_REL_YN') is not None and hd.get('MSG_ID_REL_YN') == 'Y':
                inMsgVal = returnData[hd['DT_ID']]

            del msgBytes[0:hd['DT_LEN']]

        # if inMsgType == 'LENGTH':
        #     inMsgVal = len(msgBytes)

        # mid or length 로 소켓 IN 정보 검색
        for index, inData in enumerate(systemGlobals['sokcetIn']):
            if self.initData['SK_ID'] == inData['IN_SK_ID']:
                inMid = None
                # 인 메시지가 없을 경우 바이트 길이와 길이형 메시지의 길이를 비교
                if inMsgVal == None and inData['MSG_KEY_TYPE'] == 'LENGTH':
                    inMid = msgLen
                else:
                    inMid = inMsgVal

                msgKeyVal = encodeToBytes(inData['MSG_KEY_VAL'], inData['MSG_KEY_TYPE'])
                logger.info(f'dddddddddddd : {msgKeyVal}')
                # logger.info(f'ddddddddddddf : {inMsgVal}')
                logger.info(f'ddddddddddddf : {inMid}')

                if inMid is not None:
                    if inMid == msgKeyVal:
                        inMsgId = inData['IN_MSG_ID']
                        msgInfo = inData
                        break
                else:
                    if msgKeyVal is None:
                        msgInfo = inData
                        break

        # 소켓 메시지 BODY 검색
        for index, body in enumerate(systemGlobals['socketBody']):
            if(body['MSG_ID'] == inMsgId):
                bodyList = body[body['MSG_ID']]
                break


        for index, body in enumerate(bodyList):
            if (len(msgBytes) < body['VAL_LEN']):
                raise Exception('FreeCodec convertRecieData : 바디 전문 파싱 오류')
            read = msgBytes[:body['VAL_LEN']]
            returnData[body['VAL_ID']] = decodeBytesToType(read, body['VAL_TYPE'])
            del msgBytes[0:body['VAL_LEN']]

        returnData['IN_MSG_INFO'] = msgInfo

        return returnData




