
from conf.logconfig import logger

class TestController():
    d = None

    def __init__(self):
        pass

    def recive_plc_data(self):
        try:
            logger.info('recive_plc_data ::')
        except Exception as e:
            logger.info(f'recive_plc_data exception :: {e}')



    def reciveTest(self, param):
        try:
            logger.info(f'reciveTest param : {param}')

        except Exception as e:
            logger.info(f'reciveTest Exception : {e}')