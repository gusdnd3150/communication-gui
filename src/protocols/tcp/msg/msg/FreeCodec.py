import io

from src.protocols.tcp.msg.Decoder import Decoder
import traceback
from conf.logconfig import logger
from conf.InitData_n import socketBody, sokcetIn

class FreeCodec(Decoder):

    initData = None
    hdList = []
    bodyList = socketBody
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
                # msgLen = len(copyBytes)
                # hdLen = self.initData['HD_LEN']
                # bodyLen = 0
                #
                # logger.info(f'해더 길이 : {hdLen}')
                # logger.info(f'메시지 길이 : {msgLen}')
                # for index, indata in enumerate(sokcetIn):
                #     if indata.get('IN_SK_ID') == self.initData.get('SK_ID'):
                #         # logger.info(indata.get('IN_MSG_ID'))
                #         for index, item in enumerate(socketBody):
                #             if indata.get('IN_MSG_ID') == item.get('MSG_ID'):
                #                 logger.info(item)
                #                 bodyLen = item.get('MSG_LEN')
                #
                # packetLen = hdLen+bodyLen
                # if()
                result.append(len(copyBytes))

        except Exception as e:
            logger.info(f'concyctencyCheck Exception : {e}')

        return result


    def convertRecieData(self, msgBytes):
        try:
            logger.info('convertRecieData')
            returnData = {}
            hdLen = self.hdLen
            bodyLen = 0

            logger.info(self.hdList)

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


            #
            # for body in enumerate(self.bodyList):
            #     logger.info()


        except Exception as e:
            logger.info(f'convertRecieData Exception : {e}')


        return returnData

