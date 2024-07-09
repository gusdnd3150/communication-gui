
from conf.logconfig import logger
from src.protocols.SendHandler import SendHandler
import conf.skModule as initData

class SchController():

    # guide
    # 1. logger 는 전역 로그, reciveObj['LOGGER'] 는 해당 소켓의 로그를 출력한다
    # 2. 각 reciveObj에는 ['CHANNEL'] 이 포함되어있다
    # 2.1 tcp/udp 는 sendall 로, 웹소켓은 다이렉트로 보낼 수 없다.(즉 sendHandler를 이용)
    # 3.
    sendHandler = None

    def __init__(self):
        logger.info('init schController')
        self.sendHandler = SendHandler()

    def test(self, reciveObj):
        skLogger = reciveObj['LOGGER']
        returnJson = {}
        try:
            skLogger.info(f' 스케줄 테스트 ')
            # self.sendHandler.sendSkId('TCPS_LENGTH', 'LINE_SIGNAL', returnJson)
        except Exception as e:
            skLogger.error(f'SchController.test() Exception :: {e}')
