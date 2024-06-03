
import traceback
from conf.logconfig import logger
from conf.InitData_n import sokcetList

def sendSkId(skId, msgId, data):
    try:
        for i, sk in enumerate(sokcetList):
            # logger.info(sk)
            if sk['SK_ID'] == skId:
                skThread = sk['SK_THREAD']
                handler = skThread.socket.handler
                handler.sendAllClient(handler,str('TEST').encode())
    except Exception as e:
        logger.info(f'sendSkId() Exception SK_ID:{skId} , MSG_ID:{msgId}, DATA:{data} -- {e}')


def sendBytesToSkChannel(skId, msgId, data):
    try:
        for i, sk in enumerate(sokcetList):
            # logger.info(sk)
            if sk['SK_ID'] == skId:
                skThread = sk['SK_THREAD']
                handler = skThread.socket.handler
                handler.sendAllClient(handler,str('TEST').encode())
    except Exception as e:
        logger.info(f'sendSkId() Exception SK_ID:{skId} , MSG_ID:{msgId}, DATA:{data} -- {e}')