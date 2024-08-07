import traceback

from conf.logconfig import logger
from src.protocols.SendHandler import SendHandler
import conf.skModule as skMOdule

import conf.skModule as initData
from src.utils.ExcelUtils import ExcelUtils

class TestController():

    # guide
    # 1. logger 는 전역 로그, reciveObj['LOGGER'] 는 해당 소켓의 로그를 출력한다
    # 2. 각 reciveObj에는 ['CHANNEL'] 이 포함되어있다
    # 2.1 tcp/udp 는 sendall 로 보낼 수 있지만, 웹소켓은 다이렉트로 보낼 수 없다.(즉 sendHandler를 이용)
    sendHandler = None

    def __init__(self):
        logger.info('init testcontroller')
        self.sendHandler = SendHandler()

    def recive(self, reciveObj):
        skLogger = reciveObj['LOGGER']
        Channel = reciveObj['CHANNEL']
        returnJson = {}
        try:
            # skLogger.info(f'[RECIVE TOTAL_BYTES] : {str(reciveObj["TOTAL_BYTES"])}')
            # skLogger.info(f'[RECIVE OBJ] : {reciveObj}')
            # returnJson['LINE_SIGN'] = '2'
            logger.info(f'recive Data : {reciveObj}')
        except Exception as e:
            skLogger.error(f'TestController.reciveObj() Exception :: {e}')

    def keep(self, reciveObj):
        returnJson = {}
        skLogger = reciveObj['LOGGER']
        try:
            skLogger.info(f'TestController.keep() IN_DATA : {reciveObj}')
            self.sendHandler.sendSkId('JSON_서버', 'LINE_SIGNAL', returnJson)
        except Exception as e:
            skLogger.error(f'TestController.test() Exception :: {e}')

    def idle(self, reciveObj):
        returnJson = {}
        try:
            Channel = reciveObj['CHANNEL']
            Channel.close()
        except Exception as e:
            logger.error(f'TestController.idle() Exception :: {e}')



    def testSch(self, reciveObj):
        returnJson = {}
        logger.info(f'TestController.testSch() IN_DATA : {reciveObj}')
        Channel = reciveObj['CHANNEL']
        Channel.sendall('test'.encode('utf-8'))

        try:
            returnJson['LINE_CD'] = '1'
            returnJson['LINE_SIGN'] = '2'

            SendHandler.sendSkId('SERVER1','LINE_SIGNAL',returnJson)
            SendHandler.sendSkId('TCPC_TEST', 'LINE_SIGNAL', returnJson)
        except Exception as e:
            logger.error(f'TestController.test() Exception :: {e}')




    def excel(self, reciveObj):
        skLogger = reciveObj['LOGGER']
        db = skMOdule.dbHandler

        testdata = db.getTables()
        test = ExcelUtils()
        test.makeTableList(testdata)
        try:
            skLogger.info(f'dddddddddddd')
        except Exception as e:
            skLogger.error(f'TestController.reciveObj() Exception :: {e}')


    def test(self, reciveObj):
        skLogger = reciveObj['LOGGER']
        Channel = reciveObj['CHANNEL']
        returnJson = {}
        try:
            returnJson['LINE_SIGN'] = '2'
            self.sendHandler.sendSkId('이벤트', 'LINE_SIGNAL', returnJson)
            logger.info('ssss')
        except Exception as e:
            skLogger.error(f'TestController.reciveObj() Exception :: {traceback.format_exc()}')