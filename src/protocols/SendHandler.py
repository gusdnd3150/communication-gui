
import traceback
from conf.logconfig import logger
import conf.skModule as moduleData
from src.utils.Utilitys import *

class SendHandler():

    def __init__(self):
        logger.info(f'SendHandler init')

    def sendSkId(self, skId, msgId, data):
        try:
            data['MSG_ID'] = msgId
            for i, sk in enumerate(moduleData.sokcetList):
                if sk['SK_ID'] == skId:
                    skThread = sk['SK_THREAD']
                    if sk['SK_CLIENT_TYPE'] == 'EVENT':
                        from src.protocols.tcp.ClientEventThread2 import ClientEventThread2
                        newTh = ClientEventThread2(sk, data)
                        newTh.daemon = True
                        newTh.start()
                        break
                    # if sk['SK_TYPE'] == 'WEBSK':
                    #     returnBytes = skThread.codec.encodeSendData(data)
                    #     loop = skThread.loop
                    #     asyncio.run_coroutine_threadsafe(self.send_webSk_message(skThread, returnBytes), loop)
                    #     break
                    skThread.sendMsgToAllChannels(data)
                    break
        except Exception as e:
            logger.info(f'sendSkId() Exception SK_ID:{skId} , MSG_ID:{msgId}, DATA:{data} -- {traceback.format_exc()}')
