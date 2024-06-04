
from conf.logconfig import logger

class TestController():


    def recive_plc_data(self):
        try:
            logger.info('recive_plc_data ::')
        except Exception as e:
            logger.info(f'recive_plc_data exception :: {e}')


    def test(self, reciveObj):
        try:
            logger.info(f'TestController.test() IN_DATA : {reciveObj}')

        except Exception as e:
            logger.info(f'TestController.test() Exception :: {e}')

    def reciveTest(self, param):
        try:
            logger.info(f'reciveTest param : {param}')

        except Exception as e:
            logger.info(f'reciveTest Exception : {e}')