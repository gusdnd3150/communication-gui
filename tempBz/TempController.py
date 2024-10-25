
class TempController:

    sendHandler = None
    logger = None
    dbInstance = None
    classNm = 'TempController'
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

    def sendKeepAlive(self, reciveObj):
        skLogger = reciveObj['LOGGER']
        channel = reciveObj['CHANNEL']
        thread = reciveObj['THREAD']
        skId = reciveObj['SK_ID']
        try:

            thread.sendBytesToChannel(channel, '002099990010    00  '.encode('utf-8'))
        except Exception as e:
            skLogger.error(f'TempController.sendKeepAlive() Exception :: {e}')



    def active(self, reciveObj):
        skLogger = reciveObj['LOGGER']
        channel = reciveObj['CHANNEL']
        thread = reciveObj['THREAD']
        skId = reciveObj['SK_ID']

        try:
            thread.sendBytesToChannel(channel, '002000010010    00  '.encode('utf-8'))
        except Exception as e:
            skLogger.error(f'TempController.active() Exception :: {e}')

    def recive9999(self, reciveObj):
        try:
            skLogger = reciveObj['LOGGER']
            channel = reciveObj['CHANNEL']
            thread = reciveObj['THREAD']

            returnJson = {}
            skId = reciveObj['SK_ID']
            thread.sendBytesToChannel(channel, '002000010010    00  '.encode('utf-8'))
        except Exception as e:
            skLogger.error(f'TempController.recive9999() Exception :: {e}')


    # '00570002001 0000    010000020003                         '
    def recive0002(self, reciveObj):
        skLogger = reciveObj['LOGGER']
        channel = reciveObj['CHANNEL']
        thread = reciveObj['THREAD']
        skId = reciveObj['SK_ID']
        total = str(reciveObj['TOTAL_BYTES'])

        try:
            # thread.sendMsgToChannel(channel, returnJson)
            thread.sendBytesToChannel(channel, '00200105000000000000'.encode('utf-8'))
        except Exception as e:
            skLogger.error(f'TempController.recive0002() Exception :: {e}')

    def idle(self, reciveObj):
        skLogger = reciveObj['LOGGER']
        channel = reciveObj['CHANNEL']
        thread = reciveObj['THREAD']
        skId = reciveObj['SK_ID']
        try:
            channel.close()
        except Exception as e:
            skLogger.error(f'TempController.idle() Exception :: {e}')

    def recive0061(self, reciveObj):
        skLogger = reciveObj['LOGGER']
        channel = reciveObj['CHANNEL']
        thread = reciveObj['THREAD']
        skId = reciveObj['SK_ID']
        returnJson = {}
        returnJson['MSG_ID'] = 'ATL_PF_RSLT_ACK_AND_REV_0062'
        returnJson['REV'] = '001'
        returnJson['SPARE'] = '0    00  '
        try:
            thread.sendMsgToChannel(channel, returnJson)
        except Exception as e:
            skLogger.error(f'TempController.recive0061() Exception :: {e}')


    def inactive(self, reciveObj):
        try:
            skLogger = reciveObj['LOGGER']
            channel = reciveObj['CHANNEL']

        except Exception as e:
            skLogger.error(f'TempController.inactive() Exception :: {e}')



    def recive0005(self, reciveObj):
        skLogger = reciveObj['LOGGER']
        channel = reciveObj['CHANNEL']
        thread = reciveObj['THREAD']
        resMid = reciveObj['MID_RES']
        skId = reciveObj['SK_ID']
        skLogger.info(f'TempController.recive0005 {skId} MID :: {resMid}')

        # self.accept0001Ch.append(channel)
        skLogger.info(f'total bytes {reciveObj["TOTAL_BYTES"]}')
        try:
            returnJson = {}
            returnJson['REV'] = '001'
            returnJson['SPARE'] = '0    00  '

            if resMid == '0060':  # 구독신청 완료
                skLogger.info(f' SK_ID:{skId} , 0005 MID_RES : {resMid} subscribe OK and request Job Info')
                thread.sendBytesToChannel(channel, '002000340010      00'.encode('utf-8'))
            elif resMid == '0034':
                skLogger.info(f' SK_ID:{skId} , 0005 MID_RES : {resMid} request Vin No Info')
                thread.sendBytesToChannel(channel, '003900080011      001601001102000100060'.encode('utf-8'))
            elif resMid == '0050':  # BODY 번호 송신 후 응답 수신시 잡세팅
                jobId = '01'  # 임시
                thread.sendBytesToChannel(channel, ('002200380010    00  ' + jobId).encode('utf-8'))
            elif resMid == '0038':  # job 세팅 결과 응답
                skLogger.info(f'{skId} job setting OK')
            elif resMid == '0052':  # 컨트롤러에서 인식한 바디번호 수신
                pass
            else:
                skLogger.info(f' SK_ID:{skId} , 0005 MID_RES : {resMid} None handle')

            # self.sendHandler.sendChannelMsg(channel, 'TOOL_ATL_RES_0005', returnJson)
        except Exception as e:
            skLogger.error(f'TempController.recive0005() Exception :: {e}')





    # '05380106            01060201030008177966040105LH Tire Wheel       062024-10-10:16:56:52070108Mode 01             09110011                                        1205130114115116117137.8991848.525519150.00020110.00021500.00022       130214115116117136.3491847.201319150.00020110.00021500.00022       130314115116117135.9581850.285019150.00020110.00021500.00022       130414115116117135.7501854.940119150.00020110.00021500.00022       130514115116117135.7501848.146719150.00020110.00021500.00022       2301Data No Station     I 100000037015'
    def recive0106(self, reciveObj):
        skLogger = reciveObj['LOGGER']
        channel = reciveObj['CHANNEL']
        thread = reciveObj['THREAD']
        skId = reciveObj['SK_ID']
        try:
            thread.sendBytesToChannel(channel, '002101080000000000001'.encode('utf-8'))
        except Exception as e:
            skLogger.error(f'TempController.recive0106() Exception :: {e}')


    def recive0107(self, reciveObj):
        skLogger = reciveObj['LOGGER']
        channel = reciveObj['CHANNEL']
        thread = reciveObj['THREAD']
        skId = reciveObj['SK_ID']
        try:
            thread.sendBytesToChannel(channel, '002101080000000000000'.encode('utf-8'))
        except Exception as e:
            skLogger.error(f'TempController.recive0107() Exception :: {e}')

