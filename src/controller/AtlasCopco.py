
from conf.logconfig import logger
from src.protocols.SendHandler import SendHandler
import conf.skModule as initData

class AtlasCopco():

    # guide
    # 1. logger 는 전역 로그, reciveObj['LOGGER'] 는 해당 소켓의 로그를 출력한다
    # 2. 각 reciveObj에는 ['CHANNEL'] 이 포함되어있다
    # 2.1 tcp/udp 는 sendall 로, 웹소켓은 다이렉트로 보낼 수 없다.(즉 sendHandler를 이용)
    # # returnBytes = codec.encodeSendData(returnJson)
    # channel.sendall(returnBytes)
    # self.sendHandler.sendChannelMsg(channel, 'TOOL_ATL_KEEP_9999', returnJson)
    # self.sendHandler.sendSkId('아틀라스콥코', 'TOOL_ATL_KEEP', returnJson)

    sendHandler = None

    # 0001을 보낸 채널을 보관
    accept0001Ch = []
    # 0060을 보낸 채널을 보관
    accept0060Ch = []

    def __init__(self):
        logger.info('init schController')
        self.sendHandler = SendHandler()

    def sendKeepAlive(self, reciveObj):
        skLogger = reciveObj['LOGGER']
        channel = reciveObj['CHANNEL']
        codec = reciveObj['CODEC']

        try:
            returnJson = {}
            returnJson['MSG_ID'] = 'TOOL_ATL_KEEP'
            returnJson['REV'] = '001'
            returnJson['SPARE'] = '0    00  '
            # self.sendHandler.sendChannelMsg(channel, 'TOOL_ATL_KEEP_9999', returnJson)
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
            skLogger.error(f'revKeepAlive Exception :: {e}')

    def active(self, reciveObj):
        skLogger = reciveObj['LOGGER']
        channel = reciveObj['CHANNEL']
        returnJson = {}
        returnJson['REV'] = '001'
        returnJson['SPARE'] = '0    00  '
        try:
            self.sendHandler.sendChannelMsg(channel, 'TOOL_ATL_KEEP_9999', returnJson)
        except Exception as e:
            skLogger.error(f'active Exception :: {e}')

    def recive0001(self, reciveObj):
        skLogger = reciveObj['LOGGER']
        channel = reciveObj['CHANNEL']

        self.accept0001Ch.append(channel)
        returnJson = {}
        returnJson['REV'] = '001'
        returnJson['SPARE'] = '0    00  '
        returnJson['ATLAS_COUNT'] = '11'
        returnJson['CELL_ID'] = '1234'
        returnJson['CHANNEL_ID'] = '88'
        returnJson['CTRL_NM'] = '1234567890123456789012345'
        try:
            self.sendHandler.sendChannelMsg(channel, 'TOOL_ATL_ACTV_RES_0002', returnJson)
        except Exception as e:
            skLogger.error(f'recive0001 Exception :: {e}')


    def recive0060(self, reciveObj):
        skLogger = reciveObj['LOGGER']
        channel = reciveObj['CHANNEL']
        self.accept0060Ch.append(channel)
        returnJson = {}
        returnJson['REV'] = '001'
        returnJson['SPARE'] = '0    00  '
        returnJson['MID_RES'] = reciveObj['MSG_ID']
        try:
            self.sendHandler.sendChannelMsg(channel, 'TOOL_ATL_RES_0005', returnJson)
        except Exception as e:
            skLogger.error(f'recive0060 Exception :: {e}')


    def idle(self, reciveObj):
        skLogger = reciveObj['LOGGER']
        channel = reciveObj['CHANNEL']
        self.accept0001Ch.remove(channel)
        try:
            channel.close()
        except Exception as e:
            skLogger.error(f'idle Exception :: {e}')

    def inactive(self, reciveObj):
        skLogger = reciveObj['LOGGER']
        channel = reciveObj['CHANNEL']
        self.accept0001Ch.remove(channel)
        self.accept0060Ch.remove(channel)
        try:
            skLogger.info(f'channel inactive : {channel}')
        except Exception as e:
            skLogger.error(f'inactive.test() Exception :: {e}')