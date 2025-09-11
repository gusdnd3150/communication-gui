from conf.logconfig import *

class TempController:

    sendHandler = None
    dbInstance = None
    classNm = 'TempController'
    accept0001Ch = []

    # 데이터 전송 방법
    # 
    # Channel = reciveObj['CHANNEL']
    # thread = reciveObj['THREAD']
    # 1. self.sendHandler.sendSkId(skId, msgId, data)
    # 2. thread().sendBytesToChannel(channel, '00200105000000000000'.encode('utf-8'))
    # 3. thread().sendMsgToChannel(channel, map) // map 안    MSG_ID    키: 값이    있어야함

    def __init__(self, logger, sendHandler, dbHandler=None):
        logger.info(f'TempController init')
        self.sendHandler = sendHandler
        self.dbInstance = dbHandler



    def sendKeepAlive(self, reciveObj):

        channel = reciveObj['CHANNEL']
        thread = reciveObj['THREAD']
        skId = reciveObj['SK_ID']
        try:
            returnMap ={}
            returnMap['MSG_ID'] = 'ATL_KEEPALIVE'
            returnMap['REV'] = '001'
            returnMap['SPARE'] = '0    00  '
            thread().sendMsgToChannel(channel, returnMap)
            # thread().sendBytesToChannel(channel, '002099990010    00  '.encode('utf-8'))
        except Exception as e:
            logger.error(f'TempController.sendKeepAlive() Exception :: {e}')


    def recive9999(self, reciveObj):

        channel = reciveObj['CHANNEL']
        thread = reciveObj['THREAD']
        skId = reciveObj['SK_ID']
        try:
            logger.info(f'recive9999 SK_ID is [{skId}]')
            # returnMap ={}
            # returnMap['MSG_ID'] = 'ATL_KEEPALIVE'
            # returnMap['REV'] = '001'
            # returnMap['SPARE'] = '0    00  '
            # thread().sendMsgToChannel(channel, returnMap)
            # thread().sendBytesToChannel(channel, '002099990010    00  '.encode('utf-8'))
        except Exception as e:
            logger.error(f'TempController.sendKeepAlive() Exception :: {e}')



    def active(self, reciveObj):
        
        channel = reciveObj['CHANNEL']
        thread = reciveObj['THREAD']
        skId = reciveObj['SK_ID']
        try:
            returnMap={}
            returnMap['MSG_ID'] = 'ATL_SUBCRIBE_0001'
            returnMap['REV'] = '001'
            returnMap['SPARE'] = '0    00  '
            thread().sendMsgToChannel(channel, returnMap)
            # thread().sendBytesToChannel(channel, '002000010010    00  '.encode('utf-8'))
        except Exception as e:
            logger.error(f'TempController.active() Exception :: {e}')



    def recive0002(self, reciveObj):

        channel = reciveObj['CHANNEL']
        thread = reciveObj['THREAD']
        skId = reciveObj['SK_ID']

        try:

            returnMap={}
            returnMap['MSG_ID'] = 'ATL_SUBCRIBE_0060'
            returnMap['REV'] = '001'
            returnMap['SPARE'] = '0    00  '
            thread().sendMsgToChannel(channel, returnMap)
            # thread().sendBytesToChannel(channel, '002000600010    00  '.encode('utf-8'))
        except Exception as e:
            logger.error(f'TempController.active() Exception :: {e}')


    def recive0005(self, reciveObj):

        channel = reciveObj['CHANNEL']
        thread = reciveObj['THREAD']
        skId = reciveObj['SK_ID']
        try:
            logger.info(f'recive0005 MID is [{reciveObj['ATL_MID']}]')
        except Exception as e:
            logger.error(f'TempController.active() Exception :: {e}')


    def idle(self, reciveObj):
        
        channel = reciveObj['CHANNEL']
        thread = reciveObj['THREAD']
        skId = reciveObj['SK_ID']
        try:
            channel.close()
        except Exception as e:
            logger.error(f'TempController.idle() Exception :: {e}')

