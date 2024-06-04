
import traceback
from conf.logconfig import logger

class SendHandler():

    socketList = []
    socketBody = []
    sokcetBz   = []
    sokcetIn   =[]

    def __init__(self,sokcetList,socketBody,sokcetBz,sokcetIn):
        self.socketList = sokcetList
        self.socketBody = socketBody
        self.sokcetBz = sokcetBz
        self.sokcetIn = sokcetIn

    def sendSkId(self, skId, msgId, data):
        try:
            data['MSG_ID'] = msgId
            for i, sk in enumerate(self.socketList):
                if sk['SK_ID'] == skId:
                    if sk['SK_CONN_TYPE'] == 'SERVER':
                        skThread = sk['SK_THREAD']
                        handler = skThread.socket.handler
                        handler.sendAllObjectDataClient(handler, data)

                    elif sk['SK_CONN_TYPE'] == 'CLIENT':
                        print('TODO')

        except Exception as e:
            logger.info(f'sendSkId() Exception SK_ID:{skId} , MSG_ID:{msgId}, DATA:{data} -- {e}')
