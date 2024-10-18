

class TempController2:

    sendHandler = None
    logger = None
    dbInstance = None
    classNm = 'TempController2'
    accept0001Ch = []

    # 데이터 전송 방법
    # skLogger = reciveObj['LOGGER']
    # Channel = reciveObj['CHANNEL']
    # thread = reciveObj['THREAD']
    # 1. self.sendHandler.sendSkId(skId, msgId, data)
    # 2. thread.sendBytesToChannel(channel, '00200105000000000000'.encode('utf-8'))
    # 3. thread.sendMsgToChannel(channel, map) // map 안    MSG_ID    키: 값이    있어야함

    def __init__(self, logger, sendHandler, dbHandler=None):
        logger.info(f'TempController init')
        self.sendHandler = sendHandler
        self.dbInstance = dbHandler
        self.logger = logger

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
            thread.sendMsgToChannel(Channel, returnJson2)
        except:
            print('')


    async def active(self, reciveObj):
        try:
            skLogger = reciveObj['LOGGER']
            skLogger.info(f'active ------------- ')


        except Exception as e:
            self.logger.error(f'active error :: {e}')

    async def keep(self, reciveObj):
        try:
            skLogger = reciveObj['LOGGER']
            skId= reciveObj['SK_ID']
            skLogger.info(f'keep {skId} ------------- ')

        except Exception as e:
            self.logger.error(f'active error :: {e}')

