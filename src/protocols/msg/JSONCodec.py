
import io
import traceback
from conf.logconfig import logger
import conf.skModule as moduleData
from src.utils.Utilitys import *
import json



class JSONCodec():

    initData = None
    hdList = []
    hdId = ''
    hdLen = 0
    skId = ''
    skGrp = ''
    delimiter = b''
    
    def __init__(self, initData):
        # {'PKG_ID': 'CORE', 'SK_ID': 'SERVER2', 'SK_GROUP': None, 'USE_YN': 'Y', 'SK_CONN_TYPE': 'SERVER',
        #  'SK_TYPE': 'TCP', 'SK_CLIENT_TYPE': 'KEEP', 'HD_ID': 'HD_FREE', 'SK_PORT': 5556, 'SK_IP': '0.0.0.0',
        #  'SK_DELIMIT_TYPE': '0x00', 'RELATION_VAL': None, 'SK_LOG': 'Y', 'HD_TYPE': 'FREE', 'MSG_CLASS': '',
        #  'MAX_LENGTH': 1024, 'MIN_LENGTH': 4, 'HD_LEN': 0, 'SK_THREAD': < SocketServer(Thread - 2, stopped
        # daemon
        # 34804) >}
        self.initData= initData
        self.hdId = initData['HD_ID']
        self.hdLen = initData['HD_LEN']
        self.skId = initData['SK_ID']

        if (initData.get('SK_GROUP') is not None):
            self.skGrp = initData['SK_GROUP']

        if initData.get(self.hdId) is not None:
            self.hdList = initData[self.hdId]
        if (initData['SK_DELIMIT_TYPE'] != ''):
            self.delimiter = bytes.fromhex(initData['SK_DELIMIT_TYPE'][2:])


    def concyctencyCheck(self,copyBytes):
        result = 0
        # 구분자를 통해 패킷을 나누고 패킷별로 읽어들일 개수를 배열로 반환
        start_index = -1
        end_index = -1
        brace_count = 0

        if (self.delimiter != b''):
            index = copyBytes.find(self.delimiter, 0)
            if index != -1:
                result = index + 1
        else:
            for i, char in enumerate(copyBytes):
                if char == 123: # {
                    if start_index == -1:
                        start_index = i
                    brace_count += 1
                elif char == 125: # }
                    brace_count -= 1
                    if brace_count == 0 and start_index != -1:
                        end_index = i + 1
                        break
            if (start_index > -1 and end_index > -1):
                result = end_index

        copyBytes.clear()

        return result


    def decodeRecieData(self, msgBytes):
        returnData = {}
        msgInfo = None
        inMsgVal = None
        inMsgId = None
        bodyList = None
        reciveData = json.loads(msgBytes)

        for index, hd in enumerate(self.hdList):
            if hd.get('MSG_ID_REL_YN') is not None and hd.get('MSG_ID_REL_YN') == 'Y':
                if reciveData.get(hd['DT_ID']) is not None:
                    inMsgVal = reciveData.get(hd['DT_ID'])


        # mid or length 로 소켓 IN 정보 검색
        for index, inData in enumerate(moduleData.sokcetIn):
            if self.skId == inData['IN_SK_ID'] or self.skGrp == inData['IN_SK_ID']:
                # {'PKG_ID': 'CORE', 'SK_IN_SEQ': 100, 'IN_SK_ID': 'SERVER2', 'IN_MSG_ID': 'IF_BODY',
                #  'MSG_KEY_TYPE': 'STRING', 'MSG_KEY_VAL': 'MC05', 'BZ_METHOD': 'TestController.test', 'IN_DESC': None,
                #  'USE_YN': 'Y'}
                inMid = inMsgVal
                msgKeyVal = encodeToBytes(inData['MSG_KEY_VAL'], inData['MSG_KEY_TYPE'])
                # logger.info(f' {msgKeyVal}:{inMid}')
                if inMid is not None:
                    if inMid == msgKeyVal:
                        inMsgId = inData['IN_MSG_ID']
                        msgInfo = inData
                        break
                else:
                    if msgKeyVal is None:
                        msgInfo = inData
                        break

        if reciveData is not None:
            for key, value in reciveData.items():
                returnData[key] = value

        if msgInfo is not None:
            for key, value in msgInfo.items():
                returnData[key] = value

        return returnData




    def encodeSendData(self, msgObj):
        returnData = {}
        msgId = msgObj['MSG_ID']
        msgKeyType = None
        msgKeyLen = 0
        msgKeyVal = None
        msgBody = None

        #  메시지 바디 검색
        for index, body in enumerate(moduleData.socketBody):
            if (body['MSG_ID'] == msgObj['MSG_ID']):
                # {'MSG_ID': 'LINE_SIGNAL', 'MSG_KEY_TYPE': 'STRING', 'MSG_KEY_VAL': 'LNSN', 'MSG_DB_LOG_YN': 'Y',
                # 'MSG_DESC': 'VCC', 'MSG_KEY_VAL_DESC': '', 'MSG_KEY_LENGTH': 4, 'MAX_WORK_SEC': 5,
                # 'LINE_SIGNAL': [{'MSG_ID': 'LINE_SIGNAL', 'MSG_DT_ORD': '1', 'MSG_DT_DESC': 'VCC', 'VAL_ID': 'LINE_CD',
                # 'VAL_TYPE': 'STRING', 'VAL_LEN': 4, 'VAL_DESC': ''}, {'MSG_ID': 'LINE_SIGNAL', 'MSG_DT_ORD': '2',
                # 'MSG_DT_DESC': 'VCC', 'VAL_ID': 'LINE_SIGN', 'VAL_TYPE': 'STRING', 'VAL_LEN': 1, 'VAL_DESC': ''}], 'MSG_LEN': 5}
                msgBody = body[body['MSG_ID']]
                msgKeyType = body['MSG_KEY_TYPE']
                msgKeyLen =  body['MSG_KEY_LENGTH']
                msgKeyVal = body['MSG_KEY_VAL']
                break

        if msgBody is None:
            raise Exception(f'JSONCodec encodeSendData() MSG_ID:{msgId} is None')

        # 바디 세팅
        if msgBody is not None:
            for inex, item in enumerate(msgBody):
                value = None
                if msgObj.get(item.get('VAL_ID')) is not None:
                    value = msgObj[item.get('VAL_ID')]
                returnData[item.get('VAL_ID')] = value


        # 해더 세팅
        for index, hd in enumerate(self.hdList):
            # {'HD_ID': 'HD_HS', 'DT_ORD': 1, 'DT_ID': 'TOTAL_LENGTH', 'DT_TYPE': 'INT', 'DT_LEN': 4, 'DT_NAME': '', 'DT_DESC': '',
            # 'MSG_LEN_REL_YN': 'Y', 'MSG_ID_REL_YN': '', 'DEFAULT_VALUE': ''}
            if hd.get('MSG_ID_REL_YN') is not None and hd.get('MSG_ID_REL_YN') == 'Y':
                returnData[hd['DT_ID']] = msgKeyVal

        json_str = json.dumps(returnData)
        # JSON 문자열을 바이트로 인코딩
        json_bytes = json_str.encode('utf-8')
        # 바이트를 bytearray로 변환
        returnBytes = bytearray(json_bytes)

        # 딜리미터 세팅
        if (self.delimiter != b''):
            returnBytes.extend(self.delimiter)

        return returnBytes


