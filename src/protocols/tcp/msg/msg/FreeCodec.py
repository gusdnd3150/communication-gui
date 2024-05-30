import io

from src.protocols.tcp.msg.Decoder import Decoder
import traceback
from conf.logconfig import logger

from src.utils.Container import Container
from src.utils.InitData import testBody
class FreeCodec(Decoder):

    initData = None
    hdList = []
    bodyList = []
    hdId = ''
    delimiter = b''
    hdBytes= bytearray()
    bodyBytes = bytearray()
    
    def __init__(self, initData):

        self.initData=initData
        self.hdId = initData['HD_ID']
        # InitData()
        logger.info(' 메시지 '+ str(testBody))
        
        if initData.get(self.hdId) is not None:
            self.hdList = initData[self.hdId]

        if (initData['SK_DELIMIT_TYPE'] != ''):
            self.delimiter = int(initData['SK_DELIMIT_TYPE'], 16).to_bytes(1, byteorder='big')


    def concyctencyCheck(self,copyBytes):
        result = []
        # 구분자를 통해 패킷을 나누고 패킷별로 읽어들일 개수를 배열로 반환
        try:
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


    def test(self):
        logger.info('pasing data : '+ str(self.bodyBytes))

    def setReviceBtyes(self, reciveBytes):
        try:
            logger.info('1111')

            if (self.delimiter != b''):

                # lastIndex = reciveBytes.find(self.delimiter)
                #
                # data = reciveBytes[:lastIndex+1]
                # # 읽은 바이트만큼 데이터 제거
                # del reciveBytes[:lastIndex+1]
                #
                # self.parseReciveHdBytes(data)

                messages = reciveBytes.split(self.delimiter)

                for bytes in messages:
                    if len(bytes) > 0:
                        # self.serverReviceMsgMethod(bytes, '{}:{}'.format(addr[0], str(addr[1])))
                        logger.info('revice Data : ' + str(bytes))

                        self.parseReciveHdBytes(bytes)
                        del reciveBytes[0:len(bytes) + 1]

        except:
            traceback.print_exc()


    def parseReciveHdBytes(self, bytearry):
        try:
            self.setHeaderBytes(bytearry)
            self.setBodyytes(bytearry)
        except:
            traceback.print_exc()



    def setHeaderBytes(self, bytearry):
        try:
            for index, data in enumerate(self.hdList):
                logger.info('해더 데이터 : '+str(data))

        except:
            traceback.print_exc()

    def setBodyytes(self, bytearry):
        try:

            if(len(self.bodyList) > 0):
                for index, data in enumerate(self.bodyList):
                    logger.info('해더 데이터 : ' + str(data))
            else:
                self.bodyBytes = bytearry
        except:
            traceback.print_exc()