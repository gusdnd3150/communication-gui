
from conf.logconfig import logger
from src.protocols.SendHandler import SendHandler
import conf.skModule as initData

class SchController():

    # guide
    # 데이터 전송 방법
    # skLogger = reciveObj['LOGGER']
    # Channel = reciveObj['CHANNEL']
    # thread = reciveObj['THREAD']
    # 1. SendHandler.sendSkId(skId, msgId, data)
    # 2. thread.sendBytesToChannel(channel, '00200105000000000000'.encode('utf-8'))
    # 3. thread.sendMsgToChannel(channel, map) // map 안    MSG_ID    키: 값이    있어야함

    sendHandler = None
    def __init__(self):
        logger.info('init schController')
        self.sendHandler = SendHandler()

    def test(self, reciveObj):
        skLogger = reciveObj['LOGGER']
        returnJson = {}
        try:
            skLogger.info(f' 스케줄 테스트 ')
            self.sendHandler.sendSkId('TCPS_LENGTH', 'LINE_SIGNAL', returnJson)
        except Exception as e:
            skLogger.error(f'SchController.test() Exception :: {e}')
