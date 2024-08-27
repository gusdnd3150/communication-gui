import sys
import traceback
sys.path.append('.')
from conf.logconfig import logger
if __name__ == '__main__':
    try:

        logger.info('1212')



    except:
        traceback.print_exception()

