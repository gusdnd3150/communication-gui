import io

from src.protocols.tcp.msg.Decoder import Decoder
import traceback
from conf.logconfig import logger
from conf.InitData_n import socketBody, sokcetIn
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

        msgRelYn = None
        lenRelYn = None

        for index, hd in enumerate(self.hdList):
            if (len(msgBytes) < hd['DT_LEN']):
                raise Exception('FreeCodec convertRecieData : 해더 전문 파싱 오류')
            read = msgBytes[:hd['DT_LEN']]
            returnData[hd['DT_ID']] = decodeBytes(read, hd['DT_TYPE'])
            if hd.get('MSG_LEN_REL_YN') is not None and hd.get('MSG_LEN_REL_YN') == 'Y':
                lenRelYn = returnData[hd['DT_ID']]
            if hd.get('MSG_ID_REL_YN') is not None and hd.get('MSG_ID_REL_YN') == 'Y':
                msgRelYn = returnData[hd['DT_ID']]
            del msgBytes[0:hd['DT_LEN']]

        # mid or length 로 메시지를 검색
        for index, inData in enumerate(sokcetIn):
            if self.initData['SK_ID'] == inData['IN_SK_ID']:
                # 메시지값(mid)을 우선순위로 검색
                msgKeyVal = encodeToBytes(inData['MSG_KEY_VAL'], inData['MSG_KEY_TYPE'])
                logger.info(f'메시지 키값 : {msgKeyVal}')
                if msgRelYn is not None:
                    if inData['MSG_KEY_VAL'] == msgKeyVal:
                        msgInfo = inData
                        break
                elif lenRelYn is not None:
                    if (inData['MSG_KEY_TYPE'] == 'LENGTH' and msgKeyVal == lenRelYn):
                        msgInfo = inData
                        break

        returnData['IN_MSG_INFO'] = msgInfo

        for index , body in enumerate(msgInfo):
            if (len(msgBytes) < hd['DT_LEN']):
                raise Exception('FreeCodec convertRecieData : 해더 전문 파싱 오류')
            read = msgBytes[:hd['DT_LEN']]
            returnData[hd['DT_ID']] = decodeBytes(read, hd['DT_TYPE'])
            if hd.get('MSG_LEN_REL_YN') is not None and hd.get('MSG_LEN_REL_YN') == 'Y':
                lenRelYn = returnData[hd['DT_ID']]
            if hd.get('MSG_ID_REL_YN') is not None and hd.get('MSG_ID_REL_YN') == 'Y':
                msgRelYn = returnData[hd['DT_ID']]
            del msgBytes[0:hd['DT_LEN']]

        logger.info(f'msg body : {str(msgInfo)}')


        return returnData




