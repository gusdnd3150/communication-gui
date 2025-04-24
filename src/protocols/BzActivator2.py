

import threading
import conf.skModule as systemGlobals
from conf.logconfig import *

class BzActivator2():

    bzInfo = None

    def __init__(self, bzInfo):
        self.bzInfo = bzInfo


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
                        # logger.info(f" BzActivator run : {classNm}.{methdNm} ")
                        method(self.bzInfo)
                    else:
                        logger.error(f"{self.bzInfo['SK_ID']} {methdNm} is not callable.")
                else:
                    logger.error(f'{self.bzInfo['SK_ID']} Class {classNm} not found.')
            else:
                logger.error(f'{self.bzInfo['SK_ID']} BZ_METHOD INFO is Null :')
                return
            # else:
            #     logger.error(f' BZ_INFO INFO is Null :')
            #     return
        except Exception as e:
            logger.error(f'BzActivator exception : {e}')