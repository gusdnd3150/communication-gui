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
    # 2. thread.sendBytesToChannel(channel, '00200105000000000000'.encode('utf-8'))
    # 3. thread.sendMsgToChannel(channel, map) // map 안    MSG_ID    키: 값이    있어야함

    def __init__(self, logger, sendHandler, dbHandler=None):
        logger.info(f'TempController init')
        self.sendHandler = sendHandler
        self.dbInstance = dbHandler

    def sample(self, reciveObj):
        Channel = reciveObj['CHANNEL']
        thread = reciveObj['THREAD']
        returnJson = {}
        returnJson['MSG_ID'] = ''
        try:
            logger.info(f'recive data : {reciveObj}')
            returnJson['LINE_SIGN'] = '2'
            self.sendHandler.sendSkId('TEST', 'TEST_MSG', returnJson)
            thread.sendBytesToChannel(Channel, 'sss'.encode('utf-8'))
            returnJson2 = {}
            returnJson2['MSG_ID'] = 'TEST_MSG'
            thread.sendMsgToChannel(Channel, returnJson2)
        except:
            print('')

    def sendKeepAlive(self, reciveObj):
        
        channel = reciveObj['CHANNEL']
        thread = reciveObj['THREAD']
        skId = reciveObj['SK_ID']
        returnMap ={}

        try:
            returnMap['MSG_ID'] = 'ATL_KEEPALIVE_9999'
            returnMap['REV'] = '001'
            returnMap['SPARE'] = '0    00  '
            thread().sendMsgToChannel(channel, returnMap)
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

    def recive9999(self, reciveObj):
        try:
            
            channel = reciveObj['CHANNEL']
            thread = reciveObj['THREAD']
        except Exception as e:
            logger.error(f'TempController.recive9999() Exception :: {e}')


    # '00570002001 0000    010000020003                         '
    def recive0002(self, reciveObj):
        
        channel = reciveObj['CHANNEL']
        thread = reciveObj['THREAD']
        skId = reciveObj['SK_ID']
        total = str(reciveObj['TOTAL_BYTES'])
        try:
            returnMap = {}
            toolId = skId.split('_')[0]  # 공구 아이디
            model = skId.split('_')[1]  # 모델
            if (model == 'PM'):
                thread().sendBytesToChannel(channel, '002001050000        '.encode('utf-8'))
            else: #PF6000,4000 인터페이스
                returnMap['MSG_ID'] = 'ATL_RESULT_SUBC_0060'
                returnMap['REV'] = '001'
                returnMap['SPARE'] = '0    00  '
                thread().sendMsgToChannel(channel, returnMap)
                # thread().sendBytesToChannel(channel, '002000600010        '.encode('utf-8'))

        except Exception as e:
            logger.error(f'TempController.recive0002() Exception :: {e}')


    def idle(self, reciveObj):
        
        channel = reciveObj['CHANNEL']
        thread = reciveObj['THREAD']
        skId = reciveObj['SK_ID']
        try:
            channel.close()
        except Exception as e:
            logger.error(f'TempController.idle() Exception :: {e}')

    #  ''
    def recive0061(self, reciveObj):
        
        channel = reciveObj['CHANNEL']
        thread = reciveObj['THREAD']
        skId = reciveObj['SK_ID']
        logger.info(f'recive0061 SK_ID:{skId} , data :{reciveObj}')
        returnJson = {}
        returnJson['MSG_ID'] = 'ATL_TOOL_RSLT_RES_0062'
        returnJson['REV'] = '001'
        returnJson['SPARE'] = '0    00  '
        try:
            thread().sendMsgToChannel(channel, returnJson)
        except Exception as e:
            logger.error(f'TempController.recive0061() Exception :: {e}')



    # '002400050010    00  0060'
    def recive0005(self, reciveObj):
        
        channel = reciveObj['CHANNEL']
        thread = reciveObj['THREAD']
        resMid = reciveObj['MSG_MID']
        skId = reciveObj['SK_ID']
        model = reciveObj['SK_ID'].split('_')[1]

        logger.info(f'TempController.recive0005 {skId} MID :: {resMid}')
        try:
            returnJson = {}
            returnJson['REV'] = '001'
            returnJson['SPARE'] = '0    00  '

            if resMid == '0060':  # 구독신청 완료
                logger.info(f' SK_ID:{skId} , 0005 MID_RES : {resMid} subscribe OK and request Job Info')
                if (model == 'PF'):
                    # 잡구독 파라소닉은 없음
                    returnJson['MSG_ID'] = 'ATL_JOB_SUBC_0034'
                    thread().sendMsgToChannel(channel, returnJson)
                # thread().sendBytesToChannel(channel, '002000340010      00'.encode('utf-8'))

            elif resMid == '0034':
                if (model == 'PF'):
                    # 잡구독 파라소닉은 없음
                    returnJson['MSG_ID'] = 'ATL_BODY_SUBC_0051'
                    thread().sendMsgToChannel(channel, returnJson)

            # elif resMid == '0050':  # BODY 번호 송신 후 응답 수신시 잡세팅
            #     jobId = '01'  # 임시
            #     thread().sendBytesToChannel(channel, ('002200380010    00  ' + jobId).encode('utf-8'))
            # elif resMid == '0038':  # job 세팅 결과 응답
            #     logger.info(f'{skId} job setting OK')
            # elif resMid == '0052':  # 컨트롤러에서 인식한 바디번호 수신
            #     pass
            else:
                logger.info(f' SK_ID:{skId} , 0005 MID_RES : {resMid} None handle')

            # self.sendHandler.sendChannelMsg(channel, 'TOOL_ATL_RES_0005', returnJson)
        except Exception as e:
            logger.error(f'TempController.recive0005() Exception :: {e}')





    # '05380106            01060201030008177966040105LH Tire Wheel       062024-10-10:16:56:52070108Mode 01             09110011                                        1205130114115116117137.8991848.525519150.00020110.00021500.00022       130214115116117136.3491847.201319150.00020110.00021500.00022       130314115116117135.9581850.285019150.00020110.00021500.00022       130414115116117135.7501854.940119150.00020110.00021500.00022       130514115116117135.7501848.146719150.00020110.00021500.00022       2301Data No Station     I 100000037015'
    # def recive0106(self, reciveObj):
    #     
    #     channel = reciveObj['CHANNEL']
    #     thread = reciveObj['THREAD']
    #     skId = reciveObj['SK_ID']
    #     try:
    #         thread().sendBytesToChannel(channel, '002101080000000000001'.encode('utf-8'))
    #     except Exception as e:
    #         logger.error(f'TempController.recive0106() Exception :: {e}')
    #
    #
    # def recive0107(self, reciveObj):
    #     
    #     channel = reciveObj['CHANNEL']
    #     thread = reciveObj['THREAD']
    #     skId = reciveObj['SK_ID']
    #     try:
    #         thread().sendBytesToChannel(channel, '002101080000000000000'.encode('utf-8'))
    #     except Exception as e:
    #         logger.error(f'TempController.recive0107() Exception :: {e}')
    #
