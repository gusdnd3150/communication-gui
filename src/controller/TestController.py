
from conf.logconfig import logger
# from src.protocols.SendHandler import SendHandler

# sendHandler = SendHandler()
class TestController():

    sendHandler = None
    # guide
    # 1. logger 는 전역 로그, reciveObj['LOGGER'] 는 해당 소켓의 로그를 출력한다
    # 2. 각 reciveObj에는 ['CHANNEL'] 이 포함되어있다

    def __init__(self, sendHandler):
        self.sendHandler = sendHandler
        logger.info('init testcontroller')

    def test(self, reciveObj):
        returnJson = {}
        skLogger = reciveObj['LOGGER']
        skLogger.info(f'TestController.test() IN_DATA : {reciveObj}')
        try:
            Channel = reciveObj['CHANNEL']
            Channel.sendall('active'.encode('utf-8'))
            returnJson['LINE_CD'] = '1'
            returnJson['LINE_SIGN'] = '2'
            self.sendHandler.sendSkId('SERVER1','LINE_SIGNAL',returnJson)
        except Exception as e:
            skLogger.info(f'TestController.test() Exception :: {e}')

    def keep(self, reciveObj):
        returnJson = {}
        try:
            logger.info(f'TestController.keep() IN_DATA : {reciveObj}')

        except Exception as e:
            logger.info(f'TestController.test() Exception :: {e}')

    def idle(self, reciveObj):
        returnJson = {}
        logger.info(f'TestController.idle() IN_DATA : {reciveObj}')

        try:
            Channel = reciveObj['CHANNEL']
            Channel.sendall('idle'.encode('utf-8'))
            returnJson['LINE_CD'] = 'CS01'
            returnJson['LINE_SIGN'] = '2'
            #
            self.sendHandler.sendSkId('SERVER1','LINE_SIGNAL',returnJson)
            # self.sendHandler.sendSkId('TCPC_TEST', 'LINE_SIGNAL', returnJson)
        except Exception as e:
            logger.info(f'TestController.idle() Exception :: {e}')



    def testSch(self, reciveObj):
        returnJson = {}
        logger.info(f'TestController.testSch() IN_DATA : {reciveObj}')
        Channel = reciveObj['CHANNEL']
        Channel.sendall('test'.encode('utf-8'))

        try:
            returnJson['LINE_CD'] = '1'
            returnJson['LINE_SIGN'] = '2'

            self.sendHandler.sendSkId('SERVER1','LINE_SIGNAL',returnJson)
            self.sendHandler.sendSkId('TCPC_TEST', 'LINE_SIGNAL', returnJson)
        except Exception as e:
            logger.info(f'TestController.test() Exception :: {e}')