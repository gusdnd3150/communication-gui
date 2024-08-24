
class TempController:

    sendHandler = None
    logger = None
    dbInstance = None
    classNm = 'TempController'
    accept0001Ch = []

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
            pass
            # self.sendHandler.sendChannelMsg(channel, 'TOOL_ATL_KEEP_9999', returnJson)
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
        # returnJson['ATLAS_COUNT'] = '11'
        # returnJson['CELL_ID'] = '1234'
        # returnJson['CHANNEL_ID'] = '88'
        # returnJson['CTRL_NM'] = '1234567890123456789012345'
        try:
            self.sendHandler.sendChannelMsg(channel, 'TOOL_ATL_CNN_SET_REQ_0060', returnJson)
        except Exception as e:
            skLogger.error(f'recive0001 Exception :: {e}')

    def recive0061(self, reciveObj):
        skLogger = reciveObj['LOGGER']
        channel = reciveObj['CHANNEL']
        skLogger.info(f'recive0061 result :: {reciveObj}')
        returnJson = {}
        returnJson['REV'] = '001'
        returnJson['SPARE'] = '0    00  '
        try:
            self.sendHandler.sendChannelMsg(channel, 'ATL_PF_RSLT_ACK_AND_REV_0062', returnJson)
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


    def recive0001(self, reciveObj):
        skLogger = reciveObj['LOGGER']
        channel = reciveObj['CHANNEL']
        # self.accept0001Ch.append(channel)
        try:

            returnJson = {}
            returnJson['REV'] = '001'
            returnJson['SPARE'] = '0    00  '
            returnJson['ATLAS_COUNT'] = '11'
            returnJson['CELL_ID'] = '1234'
            returnJson['CHANNEL_ID'] = '88'
            returnJson['CTRL_NM'] = '1234567890123456789012345'

            skLogger.info(f'channel inactive : {channel}')
            self.sendHandler.sendChannelMsg(channel, 'TOOL_ATL_ACTV_RES_0002', returnJson)
        except Exception as e:
            skLogger.error(f'inactive.test() Exception :: {e}')


    def recive0005(self, reciveObj):
        skLogger = reciveObj['LOGGER']
        channel = reciveObj['CHANNEL']
        skId = reciveObj['SK_ID']
        # self.accept0001Ch.append(channel)
        skLogger.info(f'total bytes {reciveObj["TOTAL_BYTES"]}')
        try:
            returnJson = {}
            returnJson['REV'] = '001'
            returnJson['SPARE'] = '0    00  '
            resMid = reciveObj['MID_RES']
            if resMid == '0060': # 구독신청 완료
                skLogger.info(f' SK_ID:{skId} , 0005 MID_RES : {resMid} subscribe OK and request Job Info')
                self.sendHandler.sendChannelBytes(channel, '002000340010      00'.encode('utf-8'))
            elif resMid == '0034':
                skLogger.info(f' SK_ID:{skId} , 0005 MID_RES : {resMid} request Vin No Info')
                self.sendHandler.sendChannelBytes(channel, '003900080011      001601001102000100060'.encode('utf-8'))
            elif resMid =='0050' : # BODY 번호 송신 후 응답 수신시 잡세팅
                jobId ='01' #임시
                self.sendHandler.sendChannelBytes(channel, ('002200380010    00  '+jobId).encode('utf-8'))
            elif resMid == '0038': # job 세팅 결과 응답
                skLogger.info(f'{skId} job setting OK')
            elif resMid =='0052': # 컨트롤러에서 인식한 바디번호 수신
                pass
            else:
                skLogger.info(f' SK_ID:{skId} , 0005 MID_RES : {resMid} None handle')

            # self.sendHandler.sendChannelMsg(channel, 'TOOL_ATL_RES_0005', returnJson)
        except Exception as e:
            skLogger.error(f' recive0005 Exception :: {e}')

    def recive0060(self, reciveObj):
        skLogger = reciveObj['LOGGER']
        channel = reciveObj['CHANNEL']
        # self.accept0001Ch.append(channel)
        try:

            returnJson = {}
            returnJson['REV'] = '001'
            returnJson['SPARE'] = '0    00  '
            returnJson['MID_RES'] = reciveObj['MSG_ID']
            skLogger.info(f'channel inactive : {channel}')
            self.sendHandler.sendChannelMsg(channel, 'TOOL_ATL_RES_0005', returnJson)
        except Exception as e:
            skLogger.error(f'inactive.test() Exception :: {e}')

    def recive0062(self, reciveObj):
        skLogger = reciveObj['LOGGER']
        channel = reciveObj['CHANNEL']
        # self.accept0001Ch.append(channel)
        try:

            returnJson = {}
            returnJson['REV'] = '001'
            returnJson['SPARE'] = '0    00  '
            returnJson['MID_RES'] = reciveObj['MSG_ID']
            skLogger.info(f'channel inactive : {channel}')
            self.sendHandler.sendChannelMsg(channel, 'TOOL_ATL_RES_0005', returnJson)
        except Exception as e:
            skLogger.error(f'inactive.test() Exception :: {e}')


    def reciveOtherBytes(self,reciveObj):
        skLogger = reciveObj['LOGGER']
        channel = reciveObj['CHANNEL']
        # self.accept0001Ch.append(channel)
        try:
            returnJson = {}
            returnJson['REV'] = '001'
            returnJson['SPARE'] = '0    00  '
            returnJson['MID_RES'] = reciveObj['MSG_ID']
            skLogger.info(f'channel inactive : {channel}')
            self.sendHandler.sendChannelBytes(channel,'tttt'.encode('utf-8'))
        except Exception as e:
            skLogger.error(f'reciveOtherBytes Exception :: {e}')