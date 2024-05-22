
import traceback
from conf.logconfig import logger


class AppController():
    d = None

    def __init__(self):
        print('AppController')


    def recive_plc_data(self):
        try:
            logger.info('recive_plc_data ::')
        except:
            logger.info('recive_plc_data exception ::')
