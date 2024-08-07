
import traceback
from conf.logconfig import logger
import conf.skModule as moduleData
import asyncio


class SendHandler():

    def __init__(self):
        logger.info(f'SendHandler init')

    def sendSkId_bk(self, skId, msgId, data):
        try:
            data['MSG_ID'] = msgId
            for i, sk in enumerate(moduleData.sokcetList):

                if sk['SK_ID'] == skId:
                    skThread = sk['SK_THREAD']
                    if sk['SK_CLIENT_TYPE'] == 'EVENT':
                        skThread.setSendData(data)
                        skThread.reSendData()
                    elif sk['SK_TYPE'] == 'WEBSK':
                        logger.info(f'{sk}')
                        returnBytes = skThread.codec.encodeSendData(data)
                        loop = skThread.loop
                        asyncio.run_coroutine_threadsafe(self.send_webSk_message(skThread, returnBytes), loop)
                    else:
                        returnBytes = skThread.codec.encodeSendData(data)
                        skThread.sendToAllChannels(returnBytes)
                    break
        except Exception as e:
            logger.info(f'sendSkId() Exception SK_ID:{skId} , MSG_ID:{msgId}, DATA:{data} -- {traceback.format_exc()}')



    def sendSkId(self, skId, msgId, data):
        try:
            data['MSG_ID'] = msgId
            for i, sk in enumerate(moduleData.sokcetList):
                if sk['SK_ID'] == skId:
                    skThread = sk['SK_THREAD']
                    if sk['SK_CLIENT_TYPE'] == 'EVENT':
                        from src.protocols.tcp.ClientEventThread import ClientEventThread
                        newTh = ClientEventThread(sk, data)
                        newTh.daemon = True
                        newTh.start()
                        break
                    if sk['SK_TYPE'] == 'WEBSK':
                        returnBytes = skThread.codec.encodeSendData(data)
                        loop = skThread.loop
                        asyncio.run_coroutine_threadsafe(self.send_webSk_message(skThread, returnBytes), loop)
                        break
                    skThread.sendMsgToAllChannels(data)
                    break
        except Exception as e:
            logger.info(f'sendSkId() Exception SK_ID:{skId} , MSG_ID:{msgId}, DATA:{data} -- {traceback.format_exc()}')

    # def sendChannelBytes(self, channel, bytes):
    #     try:
    #         channel.sendall(bytes)
    #     except Exception as e:
    #         logger.info(f'sendChannelBytes() Exception :: {e}')


    def sendChannelMsg(self, channel, msgId, data):
        try:
            data['MSG_ID'] = msgId
            for skId, ch, codec in moduleData.runChannels:
                if ch == channel:
                    # returnBytes = codec.encodeSendData(data)
                    # channel.sendall(returnBytes)
                    for i, sk in enumerate(moduleData.sokcetList):
                        if sk['SK_ID'] == skId:
                            skThread = sk['SK_THREAD']
                            skThread.sendMsgToChannel(channel,data)
                            break
                    break
        except Exception as e:
            logger.info(f'sendChannelMsg() Exception :: {traceback.format_exc()}')

    async def send_webSk_message(self, thread, returnBytes):
        await thread.sendToAllChannels(returnBytes)

