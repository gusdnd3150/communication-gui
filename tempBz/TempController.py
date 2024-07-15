


class TempController:


    sendHandler = None
    logger = None
    dbInstance = None
    classNm = 'TempController'

    def __init__(self, logger, sendHandler, dbHandler=None):
        logger.info(f'TempController init')
        self.sendHandler = sendHandler
        self.dbInstance = dbHandler
        self.logger = logger


    def reciveTest(self, reciveObj):
        sklogger = reciveObj['LOGGER']
        try:
            sklogger.info(f'reciveTest reciveObj : {reciveObj}')
            ch = reciveObj['CHANNEL']
            ch.sendall(reciveObj['TOTAL_BYTES'])
        except:
            sklogger.error(f'reciveTest')