

import threading
import conf.skModule as systemGlobals


class BzActivator():

    bzInfo = None
    logger = None  # 각 소켓별 로그

    def __init__(self, bzInfo):
        self.bzInfo = bzInfo
        self.logger = bzInfo['LOGGER']


    async def run(self):
        try:

            if (self.bzInfo.get('BZ_METHOD') is not None):
                bzClass = self.bzInfo.get('BZ_METHOD')
                classNm = bzClass.split('.')[0]
                methdNm = bzClass.split('.')[1]
                if classNm in systemGlobals.systemGlobals:
                    my_class = systemGlobals.systemGlobals[classNm]
                    method = getattr(my_class, methdNm)
                    if callable(method):
                        # self.logger.info(f" BzActivator run : {classNm}.{methdNm} ")
                        await method(self.bzInfo)
                    else:
                        self.logger.error(f" {methdNm} is not callable.")
                else:
                    self.logger.error(f'Class {classNm} not found.')
            else:
                self.logger.error(f' BZ_METHOD INFO is Null :')
                return

        except Exception as e:
            self.logger.error(f'BzActivator exception : {e}')