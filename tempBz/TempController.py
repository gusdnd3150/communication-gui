


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

    def sendKeepAlive(self, reciveObj):
        skLogger = reciveObj['LOGGER']
        channel = reciveObj['CHANNEL']
        codec = reciveObj['CODEC']

        try:
            returnJson = {}
            returnJson['MSG_ID'] = 'TOOL_ATL_KEEP'
            returnJson['REV'] = '001'
            returnJson['SPARE'] = '0    00  '
            self.sendHandler.sendChannelMsg(channel, 'TOOL_ATL_KEEP_9999', returnJson)
        except Exception as e:
            skLogger.error(f'sendKeepAlive Exception :: {e}')

    def revKeepAlive(self, reciveObj):
        skLogger = reciveObj['LOGGER']
        channel = reciveObj['CHANNEL']
        returnJson = {}
        returnJson['REV'] = reciveObj['REV']
        returnJson['SPARE'] = reciveObj['SPARE']

        try:
            self.sendHandler.sendChannelMsg(channel, 'TOOL_ATL_KEEP_9999', returnJson)
        except Exception as e:
            skLogger.error(f'revKeepAlive Exception :: {e}')

    def active(self, reciveObj):
        skLogger = reciveObj['LOGGER']
        channel = reciveObj['CHANNEL']
        returnJson = {}
        returnJson['REV'] = '001'
        returnJson['SPARE'] = '0    00  '
        try:
            self.sendHandler.sendChannelMsg(channel, 'TOOL_ATL_ACTV_REQ_0001', returnJson)
        except Exception as e:
            skLogger.error(f'active Exception :: {e}')

    def recive0002(self, reciveObj):
        skLogger = reciveObj['LOGGER']
        channel = reciveObj['CHANNEL']

        self.accept0001Ch.append(channel)
        returnJson = {}
        returnJson['REV'] = '001'
        returnJson['SPARE'] = '0    00  '
        returnJson['ATLAS_COUNT'] = '11'
        returnJson['CELL_ID'] = '1234'
        returnJson['CHANNEL_ID'] = '88'
        returnJson['CTRL_NM'] = '1234567890123456789012345'
        try:
            self.sendHandler.sendChannelMsg(channel, 'TOOL_ATL_CNN_SET_REQ_0060', returnJson)
        except Exception as e:
            skLogger.error(f'recive0001 Exception :: {e}')

    def recive0060(self, reciveObj):
        skLogger = reciveObj['LOGGER']
        channel = reciveObj['CHANNEL']
        self.accept0060Ch.append(channel)
        returnJson = {}
        returnJson['REV'] = '001'
        returnJson['SPARE'] = '0    00  '
        returnJson['MID_RES'] = reciveObj['MSG_ID']
        try:
            self.sendHandler.sendChannelMsg(channel, 'TOOL_ATL_RES_0005', returnJson)
        except Exception as e:
            skLogger.error(f'recive0060 Exception :: {e}')

    def idle(self, reciveObj):
        skLogger = reciveObj['LOGGER']
        channel = reciveObj['CHANNEL']
        self.accept0001Ch.remove(channel)
        try:
            channel.close()
        except Exception as e:
            skLogger.error(f'idle Exception :: {e}')

    def inactive(self, reciveObj):
        skLogger = reciveObj['LOGGER']
        channel = reciveObj['CHANNEL']
        self.accept0001Ch.remove(channel)
        self.accept0060Ch.remove(channel)
        try:
            skLogger.info(f'channel inactive : {channel}')
        except Exception as e:
            skLogger.error(f'inactive.test() Exception :: {e}')