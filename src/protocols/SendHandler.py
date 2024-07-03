
import traceback
from conf.logconfig import logger

# from src.protocols.tcp.ClientEventThread import ClientEventThread
import conf.InitData_n as moduleData
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
                        skThread.setSendData(data)
                        skThread.reSendData()
                    elif sk['SK_TYPE'] == 'WEBSK':
                        logger.info(f'{sk}')
                        returnBytes = skThread.codec.encodeSendData(data)
                        loop = skThread.loop
                        asyncio.run_coroutine_threadsafe(self.send_webSk_message(skThread, returnBytes), loop)
                    else:
                        # logger.info(f'sendSkId SK_DI : {sk}')
                        returnBytes = skThread.codec.encodeSendData(data)
                        skThread.sendToAllChannels(returnBytes)
                    break
        except Exception as e:
            logger.info(f'sendSkId() Exception SK_ID:{skId} , MSG_ID:{msgId}, DATA:{data} -- {traceback.format_exc()}')


    def sendChannelBytes(self, channel, bytes):
        try:
            channel.sendall(bytes)
        except Exception as e:
            logger.info(f'sendChannelBytes() Exception :: {e}')


    def sendChannelMsg(self, channel, msgId, data):
        try:
            data['MSG_ID'] = msgId
            for i, sk in enumerate(moduleData.sokcetList):
                if sk['SK_ID'] == data['SK_ID']:
                    skThread = sk['SK_THREAD']
                    returnBytes = skThread.codec.encodeSendData(data)
                    channel.sendall(returnBytes)
                    break
        except Exception as e:
            logger.info(f'sendChannelMsg() Exception :: {traceback.format_exc()}')

    async def send_webSk_message(self, thread, returnBytes):
        await thread.sendToAllChannels(returnBytes)

