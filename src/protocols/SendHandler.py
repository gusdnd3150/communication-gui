
import traceback
from conf.logconfig import logger

# from src.protocols.tcp.ClientEventThread import ClientEventThread
import conf.InitData_n as initData

class SendHandler():

    def __init__(self):
        logger.info(f'SendHandler init')

    def sendSkId(self, skId, msgId, data):
        try:
            data['MSG_ID'] = msgId
            for i, sk in enumerate(initData.sokcetList):
                if sk['SK_ID'] == skId:
                    if sk['SK_CLIENT_TYPE'] == 'EVENT':
                        skThread = sk['SK_THREAD']
                        skThread.setSendData(data)
                        skThread.reSendData()
                    else:
                        # logger.info(f'sendSkId SK_DI : {sk}')
                        skThread = sk['SK_THREAD']
                        returnBytes = skThread.codec.encodeSendData(data)
                        skThread.sendToAllChannels(returnBytes)
                    break
        except Exception as e:
            logger.info(f'sendSkId() Exception SK_ID:{skId} , MSG_ID:{msgId}, DATA:{data} -- {traceback.format_exc()}')


    def sendChannelBytes(self, channel, bytes):
        try:
            channel.sendall(bytes)
        except Exception as e:
            logger.info(f'sendChannelBytes() Exception :: {e}')


    def sendChannelMsg(self, channel, msgId, data):
        try:
            data['MSG_ID'] = msgId
            for i, sk in enumerate(initData.sokcetList):
                if sk['SK_ID'] == data['SK_ID']:
                    skThread = sk['SK_THREAD']
                    returnBytes = skThread.codec.encodeSendData(data)
                    channel.sendall(returnBytes)
                    break
        except Exception as e:
            logger.info(f'sendChannelMsg() Exception :: {traceback.format_exc()}')