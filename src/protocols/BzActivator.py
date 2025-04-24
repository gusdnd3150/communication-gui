

import threading
import conf.skModule as systemGlobals
from conf.logconfig import *


class BzActivator(threading.Thread):

    bzInfo = None

    def __init__(self, bzInfo):
        self.bzInfo = bzInfo
        super().__init__()

    def run(self):
        try:
            if (self.bzInfo.get('BZ_METHOD') is not None):
                bzClass = self.bzInfo.get('BZ_METHOD')
                classNm = bzClass.split('.')[0]
                methdNm = bzClass.split('.')[1]
                if classNm in systemGlobals.systemGlobals:
                    my_class = systemGlobals.systemGlobals[classNm]
                    method = getattr(my_class, methdNm)
                    if callable(method):
                        logger.info(f" BzActivator run : class:{classNm} / method:{methdNm} ")
                        method(self.bzInfo)
                    else:
                        logger.error(f" {methdNm} is not callable.")
                else:
                    logger.error(f'Class {classNm} not found.')
            else:
                logger.error(f' BZ_METHOD INFO is Null :')
                return
            # else:
            #     logger.error(f' BZ_INFO INFO is Null :')
            #     return
        except Exception as e:
            logger.error(f'BzActivator exception : {e}')