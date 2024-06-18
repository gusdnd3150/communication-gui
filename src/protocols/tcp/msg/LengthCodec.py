import io
import traceback
from conf.logconfig import logger
from conf.InitData_n import systemGlobals
from src.utils.Utilitys import *


class LengthCodec():
    initData = None
    hdList = []
    hdId = ''
    hdLen = 0
    skId = ''
    delimiter = b''

    def __init__(self, initData):
        # {'PKG_ID': 'CORE', 'SK_ID': 'SERVER2', 'SK_GROUP': None, 'USE_YN': 'Y', 'SK_CONN_TYPE': 'SERVER',
        #  'SK_TYPE': 'TCP', 'SK_CLIENT_TYPE': 'KEEP', 'HD_ID': 'HD_FREE', 'SK_PORT': 5556, 'SK_IP': '0.0.0.0',
        #  'SK_DELIMIT_TYPE': '0x00', 'RELATION_VAL': None, 'SK_LOG': 'Y', 'HD_TYPE': 'FREE', 'MSG_CLASS': '',
        #  'MAX_LENGTH': 1024, 'MIN_LENGTH': 4, 'HD_LEN': 0, 'SK_THREAD': < SocketServer(Thread - 2, stopped
        # daemon
        # 34804) >}
        self.initData = initData
        self.hdId = initData['HD_ID']
        self.hdLen = initData['HD_LEN']
        self.skId = initData['SK_ID']

        if initData.get(self.hdId) is not None:
            self.hdList = initData[self.hdId]
        if (initData['SK_DELIMIT_TYPE'] != ''):
            self.delimiter = bytes.fromhex(initData['SK_DELIMIT_TYPE'][2:])

    def concyctencyCheck(self, copyBytes):
        result = 0
        try:
            if (self.delimiter != b''):
                index = copyBytes.find(self.delimiter, 0)
                if index != -1:
                    result = index+1
            else:
                for index, hd in enumerate(self.hdList):
                    if (len(copyBytes) < hd['DT_LEN']):
                        raise Exception('LengthCodec convertRecieData : 해더 전문 파싱 오류')
                    read = copyBytes[:hd['DT_LEN']]
                    if hd.get('MSG_LEN_REL_YN') is not None and hd.get('MSG_LEN_REL_YN') == 'Y':
                        result = int(decodeBytesToType(read, hd['DT_TYPE']))
                    del copyBytes[0:hd['DT_LEN']]

        except Exception as e:
            logger.info(f'LengthCodec concyctencyCheck Exception : {e}')

        logger.info(f'dddddddddddd :: {result}')
        return result




    def decodeRecieData(self, msgBytes):
        returnData = {}
        msgInfo = None

        inMsgVal = None
        lenRelYn = 0
        inMsgId = None
        bodyList = None

        for index, hd in enumerate(self.hdList):
            if (len(msgBytes) < hd['DT_LEN']):
                raise Exception('LengthCodec convertRecieData : 해더 전문 파싱 오류')
            read = msgBytes[:hd['DT_LEN']]
            returnData[hd['DT_ID']] = decodeBytesToType(read, hd['DT_TYPE'])
            if hd.get('MSG_LEN_REL_YN') is not None and hd.get('MSG_LEN_REL_YN') == 'Y':
                lenRelYn = returnData[hd['DT_ID']]
            if hd.get('MSG_ID_REL_YN') is not None and hd.get('MSG_ID_REL_YN') == 'Y':
                inMsgVal = returnData[hd['DT_ID']]

            del msgBytes[0:hd['DT_LEN']]

        if inMsgVal is None:
            if self.delimiter != b'':
                inMsgVal = len(msgBytes) - 1
            else:
                inMsgVal = len(msgBytes)

        # mid or length 로 소켓 IN 정보 검색
        for index, inData in enumerate(systemGlobals['sokcetIn']):
            if self.skId == inData['IN_SK_ID']:
                # {'PKG_ID': 'CORE', 'SK_IN_SEQ': 100, 'IN_SK_ID': 'SERVER2', 'IN_MSG_ID': 'IF_BODY',
                #  'MSG_KEY_TYPE': 'STRING', 'MSG_KEY_VAL': 'MC05', 'BZ_METHOD': 'TestController.test', 'IN_DESC': None,
                #  'USE_YN': 'Y'}
                inMid = None
                # 인 메시지가 없을 경우 바이트 길이와 길이형 메시지의 길이를 비교
                if inData['MSG_KEY_TYPE'] == 'LENGTH':
                    if inMsgVal == encodeToBytes(inData['MSG_KEY_VAL'], inData['MSG_KEY_TYPE']):
                        inMid = inMsgVal
                else:
                   inMid = inMsgVal

                msgKeyVal = encodeToBytes(inData['MSG_KEY_VAL'], inData['MSG_KEY_TYPE'])
                logger.info(f'inMid:{inMid}  msgKeyVal:{msgKeyVal}')
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
            if (body['MSG_ID'] == inMsgId):
                bodyList = body[body['MSG_ID']]
                break

        for index, body in enumerate(bodyList):
            if (len(msgBytes) < body['VAL_LEN']):
                raise Exception('LengthCodec convertRecieData : 바디 전문 파싱 오류')
            read = msgBytes[:body['VAL_LEN']]
            returnData[body['VAL_ID']] = decodeBytesToType(read, body['VAL_TYPE'])
            del msgBytes[0:body['VAL_LEN']]

        returnData['BZ_INFO'] = msgInfo

        return returnData

    def encodeSendData(self, msgObj):
        returnBytes = bytearray()
        try:
            msgId = msgObj['MSG_ID']
            msgKeyType = None
            msgKeyLen = 0
            msgKeyVal = None
            msgBody = None

            bodyBytes = bytearray()
            headerBytes = bytearray()

            #  메시지 바디 검색
            for index, body in enumerate(systemGlobals['socketBody']):
                if (body['MSG_ID'] == msgObj['MSG_ID']):
                    # {'MSG_ID': 'LINE_SIGNAL', 'MSG_KEY_TYPE': 'STRING', 'MSG_KEY_VAL': 'LNSN', 'MSG_DB_LOG_YN': 'Y',
                    # 'MSG_DESC': 'VCC', 'MSG_KEY_VAL_DESC': '', 'MSG_KEY_LENGTH': 4, 'MAX_WORK_SEC': 5,
                    # 'LINE_SIGNAL': [{'MSG_ID': 'LINE_SIGNAL', 'MSG_DT_ORD': '1', 'MSG_DT_DESC': 'VCC', 'VAL_ID': 'LINE_CD',
                    # 'VAL_TYPE': 'STRING', 'VAL_LEN': 4, 'VAL_DESC': ''}, {'MSG_ID': 'LINE_SIGNAL', 'MSG_DT_ORD': '2',
                    # 'MSG_DT_DESC': 'VCC', 'VAL_ID': 'LINE_SIGN', 'VAL_TYPE': 'STRING', 'VAL_LEN': 1, 'VAL_DESC': ''}], 'MSG_LEN': 5}
                    msgBody = body[body['MSG_ID']]
                    msgKeyType = body['MSG_KEY_TYPE']
                    msgKeyLen = body['MSG_KEY_LENGTH']
                    msgKeyVal = body['MSG_KEY_VAL']
                    break

            if msgBody is None:
                raise Exception(f'LengthCodec encodeSendData() MSG_ID:{msgId} is None')

            # 메시지 바디 세팅
            for index, body in enumerate(msgBody):
                value = None
                if msgObj.get(body['VAL_ID']) is not None:
                    value = msgObj[body['VAL_ID']]
                bodyBytes.extend(encodeDataToBytes(value, body['VAL_TYPE'], body['VAL_LEN']))

            totalLen = len(bodyBytes) + self.hdLen

            # 해더 세팅
            for index, hd in enumerate(self.hdList):
                # {'HD_ID': 'HD_HS', 'DT_ORD': 1, 'DT_ID': 'TOTAL_LENGTH', 'DT_TYPE': 'INT', 'DT_LEN': 4, 'DT_NAME': '', 'DT_DESC': '',
                # 'MSG_LEN_REL_YN': 'Y', 'MSG_ID_REL_YN': '', 'DEFAULT_VALUE': ''}
                if hd.get('MSG_LEN_REL_YN') is not None and hd.get('MSG_LEN_REL_YN') == 'Y':
                    headerBytes.extend(encodeDataToBytes(totalLen, hd['DT_TYPE'], hd['DT_LEN'], '0'))
                elif hd.get('MSG_ID_REL_YN') is not None and hd.get('MSG_ID_REL_YN') == 'Y':
                    headerBytes.extend(encodeDataToBytes(msgKeyVal, msgKeyType, msgKeyLen))
                else:
                    value = None
                    if msgObj.get(hd['DT_ID']) is not None and msgObj.get(hd['DT_ID']) != '':
                        value = msgObj.get(hd['DT_ID'])
                    elif hd['DEFAULT_VALUE'] is not None and hd['DEFAULT_VALUE'] != '':
                        value = hd['DEFAULT_VALUE']
                    headerBytes.extend(encodeDataToBytes(value, hd['DT_TYPE'], hd['DT_LEN']))

            returnBytes = headerBytes + bodyBytes

            # 딜리미터 세팅
            if (self.delimiter != b''):
                returnBytes.extend(self.delimiter)

            return returnBytes
        except Exception as e:
            logger.info(f'LengthCodec encodeSendData() Exception :: {e}')


