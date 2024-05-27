import io

from src.protocols.tcp.msg.Decoder import Decoder
import traceback
from conf.logconfig import logger
class FreeCodec(Decoder):

    initData = None
    hdList = []
    hdId = ''
    delimiter =b''

    def __init__(self, initData):
        self.initData=initData
        self.hdId = initData['HD_ID']
        self.hdList = initData[self.hdId]

        if (initData['SK_DELIMIT_TYPE'] != ''):
            self.delimiter = int(initData['SK_DELIMIT_TYPE'], 16)

    def concyctencyCheck(self,copyBytes):
        result = False

        try:
            logger.info('test'+ str(copyBytes))
            # messages = dataBuf.split(b"\x00")
            messages = copyBytes.split(self.delimiter)
            if len(messages) > 1:
                result = True
        except:
            traceback.print_exc()

        return result