
from conf.logconfig import logger
from src.protocols.SendHandler import SendHandler
import conf.skModule as initData

class AtlasCopco():

    # guide
    # 1. logger 는 전역 로그, reciveObj['LOGGER'] 는 해당 소켓의 로그를 출력한다
    # 2. 각 reciveObj에는 ['CHANNEL'] 이 포함되어있다
    # 2.1 tcp/udp 는 sendall 로, 웹소켓은 다이렉트로 보낼 수 없다.(즉 sendHandler를 이용)
    # # returnBytes = codec.encodeSendData(returnJson)
    #             # channel.sendall(returnBytes)
    #             self.sendHandler.sendChannelMsg(channel, 'TOOL_ATL_KEEP_9999', returnJson)
    #             # self.sendHandler.sendSkId('아틀라스콥코', 'TOOL_ATL_KEEP', returnJson)
    sendHandler = None

    def __init__(self):
        logger.info('init schController')
        self.sendHandler = SendHandler()

    def sendKeepAlive(self, reciveObj):
        skLogger = reciveObj['LOGGER']
        channel = reciveObj['CHANNEL']
        codec = reciveObj['CODEC']

        returnJson = {}
        returnJson['MSG_ID'] = 'TOOL_ATL_KEEP'
        returnJson['REV'] = '001'
        returnJson['SPARE'] = '0    00  '
        try:
            # returnBytes = codec.encodeSendData(returnJson)
            # channel.sendall(returnBytes)
            self.sendHandler.sendChannelMsg(channel, 'TOOL_ATL_KEEP_9999', returnJson)
            # self.sendHandler.sendSkId('아틀라스콥코', 'TOOL_ATL_KEEP', returnJson)
        except Exception as e:
            skLogger.error(f'sendKeepAlive Exception :: {e}')


    def revKeepAlive(self,reciveObj):
        skLogger = reciveObj['LOGGER']
        channel = reciveObj['CHANNEL']
        returnJson = {}
        returnJson['REV'] = reciveObj['REV']
        returnJson['SPARE'] = reciveObj['SPARE']
        try:
            self.sendHandler.sendChannelMsg(channel, 'TOOL_ATL_KEEP_9999', returnJson)
        except Exception as e:
            skLogger.error(f'revKeepAlive.test() Exception :: {e}')

    def active(self, reciveObj):
        skLogger = reciveObj['LOGGER']
        channel = reciveObj['CHANNEL']
        returnJson = {}
        returnJson['REV'] = '001'
        returnJson['SPARE'] = '0    00  '
        try:
            self.sendHandler.sendChannelMsg(channel, 'TOOL_ATL_ACTV_REQ_0001', returnJson)
        except Exception as e:
            skLogger.error(f'active Exception :: {e}')

    def recive0002(self, reciveObj):
        skLogger = reciveObj['LOGGER']
        channel = reciveObj['CHANNEL']

        returnJson = {}
        returnJson['REV'] = '001'
        returnJson['SPARE'] = '0    00  '
        try:
            # self.sendHandler.sendChannelMsg(channel, 'TOOL_ATL_ACTV_REQ_0001', returnJson)
            skLogger.info(f'fffffffffffffff')
        except Exception as e:
            skLogger.error(f'active Exception :: {e}')