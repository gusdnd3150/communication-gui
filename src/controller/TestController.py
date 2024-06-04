
from conf.logconfig import logger
# from src.protocols.SendHandler import SendHandler

# sendHandler = SendHandler()
class TestController():

    sendHandler = None

    def __init__(self, sendHandler):
        self.sendHandler = sendHandler
        logger.info('init testcontroller')

    def test(self, reciveObj):
        try:
            logger.info(f'TestController.test() IN_DATA : {reciveObj}')
            self.sendHandler.sendSkId('TCPS_TEST','','None')
        except Exception as e:
            logger.info(f'TestController.test() Exception :: {e}')
