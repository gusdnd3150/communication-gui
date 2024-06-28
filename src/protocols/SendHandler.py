
import traceback
from conf.logconfig import logger

# from src.protocols.tcp.ClientEventThread import ClientEventThread


class SendHandler():

    socketList = []
    socketBody = []
    sokcetBz   = []
    sokcetIn   = []

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
                    if sk['SK_CLIENT_TYPE'] == 'EVENT':
                        skThread = sk['SK_THREAD']
                        logger.info(f'event 스레드 : {skThread}')
                        skThread.sendData = skThread.codec.encodeSendData(data)
                        logger.info(f'event 스레드 : {skThread.sendData}')
                        # skThread.sendToAllChannels(returnBytes)
                    else:
                        # logger.info(f'sendSkId SK_DI : {sk}')
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


    def sendChannelMsg(self, channel, msgId, data):
        try:
            data['MSG_ID'] = msgId
            for i, sk in enumerate(self.socketList):
                if sk['SK_ID'] == data['SK_ID']:
                    # logger.info(f'sendSkId SK_DI : {sk}')
                    skThread = sk['SK_THREAD']
                    returnBytes = skThread.codec.encodeSendData(data)
                    channel.sendall(returnBytes)
                    break
        except Exception as e:
            logger.info(f'sendChannelMsg() Exception :: {e}')