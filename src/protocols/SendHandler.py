
import traceback
from conf.logconfig import logger
import conf.skModule as moduleData
import asyncio


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

    # def sendChannelMsg(self, channel, msgId, data):
    #     try:
    #         data['MSG_ID'] = msgId
    #         for skId, ch, thread in moduleData.runChannels:
    #             if ch == channel:
    #                 logger.info(f'thread ty : {thread.skclientTy}')
    #                 thread.sendMsgToChannel(channel,data)
    #                 # for i, sk in enumerate(moduleData.sokcetList):
    #                 #     if sk['SK_ID'] == skId:
    #                 #         skThread = sk['SK_THREAD']
    #                 #         skThread.sendMsgToChannel(channel,data)
    #                 #         break
    #                 break
    #     except Exception as e:
    #
    #         logger.info(f'sendChannelMsg() Exception :: {traceback.format_exc()}')
    #
    #
    # def sendChannelBytes(self, channel, bytes):
    #     try:
    #         for skId, ch, thread in moduleData.runChannels:
    #             if ch == channel:
    #                 logger.info(f'thread ty : {thread.skclientTy}')
    #                 thread.sendBytesToChannel(channel, bytes)
    #                 # for i, sk in enumerate(moduleData.sokcetList):
    #                 #     if sk['SK_ID'] == skId:
    #                 #         skThread = sk['SK_THREAD']
    #                 #         skThread.sendBytesToChannel(channel,bytes)
    #                 #         break
    #                 break
    #     except Exception as e:
    #         logger.info(f'sendChannelMsg() Exception :: {traceback.format_exc()}')

    async def send_webSk_message(self, thread, returnBytes):
        await thread.sendBytes(returnBytes)

