import traceback

from conf.logconfig import logger
from src.protocols.SendHandler import SendHandler
import conf.skModule as skMOdule

import conf.skModule as initData
from src.utils.ExcelUtils import ExcelUtils
import time
class TestController():

    # guide
    # 데이터 전송 방법
    # skLogger = reciveObj['LOGGER']
    # Channel = reciveObj['CHANNEL']
    # thread = reciveObj['THREAD']
    # 1. SendHandler.sendSkId(skId, msgId, data)
    # 2. thread.sendBytesToChannel(channel, '00200105000000000000'.encode('utf-8'))
    # 3. thread.sendMsgToChannel(channel, map) // map 안    MSG_ID    키: 값이    있어야함

    sendHandler = None

    def __init__(self):
        logger.info('init testcontroller')
        self.sendHandler = SendHandler()

    def sample(self, reciveObj):
        skLogger = reciveObj['LOGGER']
        Channel = reciveObj['CHANNEL']
        thread = reciveObj['THREAD']
        returnJson = {}
        returnJson['MSG_ID'] = ''
        try:
            skLogger.info(f'recive data : {reciveObj}')
            returnJson['LINE_SIGN'] = '2'
            self.sendHandler.sendSkId('TEST', 'TEST_MSG', returnJson)
            thread.sendBytesToChannel(Channel, 'sss'.encode('utf-8'))
            returnJson2 = {}
            returnJson2['MSG_ID'] = 'TEST_MSG'
            thread.sendMsgToChannel(Channel,returnJson2)
            thread.sendMsgToAllChannels(returnJson)
        except:
            logger.error(f'sample exception : {traceback.format_exc()}')


    def reciveWeb(self, reciveObj):
        skLogger = reciveObj['LOGGER']
        Channel = reciveObj['CHANNEL']
        thread = reciveObj['THREAD']
        # path = reciveObj['PATH']
        returnJson = {}

        try:
            skLogger.info(f'recive data : {reciveObj}')
            returnJson['MSG_ID'] = 'TEST_MSG'
            returnJson['LINE_SIGN'] = '2'
            self.sendHandler.sendSkId('TEST', 'TEST_MSG', returnJson)
            # thread.sendBytesToChannel(Channel, 'sss'.encode('utf-8'))
            # returnJson2 = {}
            # returnJson2['MSG_ID'] = 'TEST_MSG'
            thread.sendMsgToChannel(Channel,returnJson)
            # thread.sendMsgToAllChannels(returnJson)
        except:
            logger.error(f'sample exception : {traceback.format_exc()}')

    def recive(self, reciveObj):
        skLogger = reciveObj['LOGGER']
        Channel = reciveObj['CHANNEL']
        thread = reciveObj['THREAD']
        returnJson = {}
        skLogger.info(f'recive data : {reciveObj}')

        try:
            test = reciveObj['TOTAL_BYTES'].decode('utf-8')
            # skLogger.info(f'[RECIVE TOTAL_BYTES] : {str(reciveObj["TOTAL_BYTES"])}')
            skLogger.info(f'[RECIVE OBJ] : {test}')
            returnJson['LINE_SIGN'] = '2'
            # self.sendHandler.sendSkId('WEB_SK_TEST','TEST_MSG',returnJson)
            # thread.sendBytesToChannel(Channel, 'sss'.encode('utf-8'))


        except Exception as e:
            skLogger.error(f'TestController.reciveObj() Exception :: {e}')

    def active(self, reciveObj):
        skLogger = reciveObj['LOGGER']
        Channel = reciveObj['CHANNEL']
        skLogger.info('active gogo')
        try:
            returnJson = {}
            # skLogger.info(f'[RECIVE TOTAL_BYTES] : {str(reciveObj["TOTAL_BYTES"])}')
            # skLogger.info(f'[RECIVE OBJ] : {reciveObj}')
            # returnJson['LINE_SIGN'] = '2'
        except Exception as e:
            skLogger.error(f'TestController.reciveObj() Exception :: {e}')

    def keep(self, reciveObj):
        returnJson = {}
        skLogger = reciveObj['LOGGER']
        channel = reciveObj['CHANNEL']
        thread = reciveObj['THREAD']
        try:
            # self.sendHandler.sendSkId('JSON_서버', 'LINE_SIGNAL', returnJson)
            thread.sendBytesToChannel(channel, 'sss'.encode('utf-8'))
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
        except Exception as e:
            skLogger.error(f'TestController.reciveObj() Exception :: {traceback.format_exc()}')