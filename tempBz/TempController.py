


class TempController:


    sendHandler = None
    logger = None
    classNm = 'TempController'

    def __init__(self, logger, sendHandler):
        logger.info(f'TempController init')
        self.sendHandler = sendHandler
        self.logger = logger


    def reciveTest(self, reciveObj):
        try:
            self.logger.info(f'reciveTest reciveObj : {reciveObj}')
            ch = reciveObj['CHANNEL']
            ch.sendall(reciveObj['TOTAL_BYTES'])
        except:
            self.logger.error(f'reciveTest')