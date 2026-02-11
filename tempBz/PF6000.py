
class PF6000:

    sendHandler = None
    dbInstance = None
    classNm = 'PF6000'
    accept0001Ch = []
    logger=None

    # 데이터 전송 방법
    # Channel = reciveObj['CHANNEL']
    # thread = reciveObj['THREAD']
    # skId = reciveObj['SK_ID']
    # 1. self.sendHandler.sendSkId(skId, msgId, data)
    # 2. thread().sendBytesToChannel(channel, '00200105000000000000'.encode('utf-8'))
    # 3. thread().sendMsgToChannel(channel, map) // map 안    MSG_ID    키: 값이    있어야함

    def __init__(self, logger, sendHandler, dbHandler=None):
        self.logger = logger
        self.sendHandler = sendHandler
        self.dbInstance = dbHandler
        self.logger.info(f'PF6000 init')


    def send9999(self, reciveObj):
        channel = reciveObj['CHANNEL']
        thread = reciveObj['THREAD']
        skId = reciveObj['SK_ID']
        try:
            returnMap ={}
            returnMap['MSG_ID'] = 'PF6000_9999'
            returnMap['REV'] = '001'
            returnMap['SPARE'] = '0    00  '
            thread().sendMsgToChannel(channel, returnMap)
            # thread().sendBytesToChannel(channel, '002099990010    00  '.encode('utf-8'))
        except Exception as e:
            self.logger.error(f'TempController.sendKeepAlive() Exception :: {e}')


    def receive9999(self, reciveObj):
        channel = reciveObj['CHANNEL']
        thread = reciveObj['THREAD']
        skId = reciveObj['SK_ID']
        try:
            self.logger.info(f'recive9999 SK_ID is [{skId}]')
            # returnMap ={}
            # returnMap['MSG_ID'] = 'PF6000_9999'
            # returnMap['REV'] = '001'
            # returnMap['SPARE'] = '0    00  '
            # thread().sendMsgToChannel(channel, returnMap)
            # thread().sendBytesToChannel(channel, '002099990010    00  '.encode('utf-8'))
        except Exception as e:
            self.logger.error(f'TempController.sendKeepAlive() Exception :: {e}')



    def active(self, reciveObj):
        channel = reciveObj['CHANNEL']
        thread = reciveObj['THREAD']
        skId = reciveObj['SK_ID']
        try:
            returnMap={}
            returnMap['MSG_ID'] = 'PF6000_0001'
            returnMap['REV'] = '001'
            returnMap['SPARE'] = '0    00  '
            thread().sendMsgToChannel(channel, returnMap)
            # thread().sendBytesToChannel(channel, '002000010010    00  '.encode('utf-8'))
        except Exception as e:
            self.logger.error(f'TempController.active() Exception :: {e}')



    def receive0002(self, reciveObj):
        channel = reciveObj['CHANNEL']
        thread = reciveObj['THREAD']
        skId = reciveObj['SK_ID']
        try:
            returnMap={}
            returnMap['MSG_ID'] = 'PF6000_0060'
            returnMap['REV'] = '001'
            returnMap['SPARE'] = '0    00  '
            thread().sendMsgToChannel(channel, returnMap)
            # thread().sendBytesToChannel(channel, '002000600010    00  '.encode('utf-8'))
        except Exception as e:
            self.logger.error(f'TempController.active() Exception :: {e}')


    def receive0005(self, reciveObj):

        channel = reciveObj['CHANNEL']
        thread = reciveObj['THREAD']
        skId = reciveObj['SK_ID']
        try:
            self.logger.info(f'receive0005 MID is [{reciveObj['MID_NUM']}]')
        except Exception as e:
            self.logger.error(f'TempController.active() Exception :: {e}')



    def idle(self, reciveObj):
        channel = reciveObj['CHANNEL']
        thread = reciveObj['THREAD']
        skId = reciveObj['SK_ID']
        try:
            channel.close()
        except Exception as e:
            self.logger.error(f'TempController.idle() Exception :: {e}')

