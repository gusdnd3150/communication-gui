
from conf.logconfig import logger
from src.protocols.SendHandler import SendHandler
import conf.skModule as initData

class AtlasCopco():

    # guide
    # 1. logger 는 전역 로그, reciveObj['LOGGER'] 는 해당 소켓의 로그를 출력한다
    # 2. 각 reciveObj에는 ['CHANNEL'] 이 포함되어있다
    # 2.1 tcp/udp 는 sendall 로, 웹소켓은 다이렉트로 보낼 수 없다.(즉 sendHandler를 이용)
    # 3.
    sendHandler = None

    def __init__(self):
        logger.info('init schController')
        self.sendHandler = SendHandler()

    def keepAlive(self, reciveObj):
        skLogger = reciveObj['LOGGER']
        channel = reciveObj['CHANNEL']
        codec = reciveObj['CODEC']

        returnJson = {}
        returnJson['MSG_ID'] = 'TOOL_ATL_KEEP'
        returnJson['REV'] = '001'
        returnJson['SPARE'] = '000000000'
        try:
            skLogger.info(f'채널 정보 : {channel}')
            returnBytes = codec.encodeSendData(returnJson)
            channel.sendall(returnBytes)
            # self.sendHandler.sendChannelMsg(channel, 'TOOL_ATL_KEEP', returnJson)
            # self.sendHandler.sendSkId('아틀라스콥코', 'TOOL_ATL_KEEP', returnJson)
        except Exception as e:
            skLogger.error(f'keepAlive.test() Exception :: {e}')
