
class Temp:

    sendHandler = None
    logger = None
    dbInstance = None
    classNm = 'Temp'
    accept0001Ch = []

    # 데이터 전송 방법
    # skLogger = reciveObj['LOGGER']
    # Channel = reciveObj['CHANNEL']
    # thread = reciveObj['THREAD']
    # 1. SendHandler.sendSkId(skId, msgId, data)
    # 2. thread.sendBytesToChannel(channel, '00200105000000000000'.encode('utf-8'))
    # 3. thread.sendMsgToChannel(channel, map) // map 안    MSG_ID    키: 값이    있어야함

    def __init__(self, logger, sendHandler, dbHandler=None):
        logger.info(f'Temp init')
        self.sendHandler = sendHandler
        self.dbInstance = dbHandler
        self.logger = logger


    def recive(self, reciveObj):
        skLogger = reciveObj['LOGGER']
        channel = reciveObj['CHANNEL']
        thread = reciveObj['THREAD']
        skId = reciveObj['SK_ID']
        try:
            skLogger.info(f'recive data  {skId}  : {reciveObj['TOTAL_BYTES']}')
            #thread.sendMsgToChannel(channel, returnJson)
        except Exception as e:
            skLogger.error(f'TempController.recive0061() Exception :: {e}')

