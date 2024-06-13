
import traceback
from conf.logconfig import logger

class SendHandler():

    socketList = []
    socketBody = []
    sokcetBz   = []
    sokcetIn   =[]

    def __init__(self,sokcetList,socketBody,sokcetBz,sokcetIn):
        self.socketList = sokcetList
        self.socketBody = socketBody
        self.sokcetBz = sokcetBz
        self.sokcetIn = sokcetIn

    def sendSkId(self, skId, msgId, data):
        try:
            data['MSG_ID'] = msgId
            for i, sk in enumerate(self.socketList):
                if sk['SK_ID'] == skId:
                    logger.info(f'sendSkId SK_DI : {sk}')
                    skThread = sk['SK_THREAD']
                    returnBytes = skThread.codec.encodeSendData(data)
                    skThread.sendToAllChannels(returnBytes)
                    break
        except Exception as e:
            logger.info(f'sendSkId() Exception SK_ID:{skId} , MSG_ID:{msgId}, DATA:{data} -- {e}')


    def sendChannelBytes(self, channel, bytes):
        try:
            channel.sendall(bytes)
        except Exception as e:
            logger.info(f'sendChannelBytes() Exception :: {e}')
