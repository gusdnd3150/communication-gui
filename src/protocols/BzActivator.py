

import threading
from conf.logconfig import logger
from conf.InitData_n import systemGlobals

class BzActivator(threading.Thread):

    bzInfo = None
    skGroup = None

    def __init__(self, bzInfo):
        self.bzInfo = bzInfo
        if bzInfo.get('SK_GROUP') is not None:
            self.skGroup = bzInfo['SK_GROUP']
        super().__init__()

    def run(self):
        try:
            # logger.info(f'BzActivator run() parmas :: {self.bzInfo}')
            if (self.bzInfo.get('BZ_INFO') is not None):
                if (self.bzInfo.get('BZ_INFO').get('BZ_METHOD') is not None):
                    bzClass = self.bzInfo.get('BZ_INFO').get('BZ_METHOD')
                    classNm = bzClass.split('.')[0]
                    methdNm = bzClass.split('.')[1]
                    if classNm in systemGlobals:
                        my_class = systemGlobals[classNm]
                        method = getattr(my_class, methdNm)
                        if callable(method):
                            logger.info(f"SK_GROUP:{self.skGroup} onReciveData : {classNm}.{methdNm} call.")
                            method(self.bzInfo)
                        else:
                            logger.error(f"SK_GROUP:{self.skGroup} {methdNm} is not callable.")
                    else:
                        logger.error(f"SK_GROUP:{self.skGroup} Class {classNm} not found.")
                else:
                    logger.error(f'SK_GROUP:{self.skGroup} BZ_METHOD INFO is Null :')
                    return
            else:
                logger.error(f'SK_GROUP:{self.skGroup} BZ_INFO INFO is Null :')
                return
        except Exception as e:
            logger.error(f'SK_GROUP:{self.skGroup} BzActivator exception : {e}')