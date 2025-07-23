import threading
from conf.logconfig import *
from src.protocols.asyncPro.AsynFn import *
import traceback
import conf.skModule as moduleData

class AsyncSocket(threading.Thread):

    def __init__(self):
        super(AsyncSocket,self).__init__()
        self._stop_event = threading.Event()

    def __del__(self):
        logger.info(f'AsyncSocket is deleted')

    def run(self):
        self.initServerClient()

    def stop(self):
        try:
            logger.info(f'stoped')
        except Exception as e:
            logger.error(f'SK_ID:{self.skId} Stop fail : {traceback.format_exc()}')




    def initServerClient(self):
        try:
            print('test')
            asyncio.run(main())
        except Exception as e:
            logger.error(f'TCP SERVER Bind exception : SK_ID={self.skId}  : {e}')

