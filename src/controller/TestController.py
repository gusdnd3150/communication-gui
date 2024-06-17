
from conf.logconfig import logger
# from src.protocols.SendHandler import SendHandler

# sendHandler = SendHandler()
class TestController():

    sendHandler = None

    def __init__(self, sendHandler):
        self.sendHandler = sendHandler
        logger.info('init testcontroller')

    def test(self, reciveObj):
        returnJson = {}
        logger.info(f'TestController.test() IN_DATA : {reciveObj}')
        try:
            Channel = reciveObj['CHANNEL']
            Channel.sendall('active'.encode('utf-8'))
            returnJson['LINE_CD'] = '1'
            returnJson['LINE_SIGN'] = '2'
            #
            self.sendHandler.sendSkId('SERVER1','LINE_SIGNAL',returnJson)
        except Exception as e:
            logger.info(f'TestController.test() Exception :: {e}')


    def idle(self, reciveObj):
        returnJson = {}
        logger.info(f'TestController.idle() IN_DATA : {reciveObj}')

        try:
            Channel = reciveObj['CHANNEL']
            Channel.sendall('idle'.encode('utf-8'))
            # returnJson['LINE_CD'] = '1'
            # returnJson['LINE_SIGN'] = '2'
            #
            # self.sendHandler.sendSkId('SERVER1','LINE_SIGNAL',returnJson)
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