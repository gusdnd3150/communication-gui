from conf.logconfig import logger
import gc
import sqlite3
from conf.QueryString import *
from src.controller.TestController import TestController
from src.protocols.SendHandler import SendHandler

ctrList = []

logger.info('DB connectiom with SqlLite')
dbInstance = sqlite3.connect('core.db')


useYnCombo = ['Y','N']
skTypeCombo = ['TCP','UDP','WEBSK']
skConnCombo = ['SERVER','CLIENT']
skClientCombo = ['KEEP','EVENT']
hdCombo = ['LENGTH_STR_8B','LENGTH_STR_20B','LENGTH_20B','FREE','JSON']


sokcetList = []
socketHd = []
socketHdDt = []
socketBody = []
socketBodyDt = []
socketVal = []
# sokcetBz = getsokcetBz()
sokcetBz = []
sokcetIn = []
sokcetInToOut = []
sokcetOut = []
sokcetSub = []
sokcetSch = []
mainLayout = None
systemGlobals = globals()
systemGlobals['mainLayout'] = None
systemGlobals['mainInstance'] = None


def getsokcetList(pkgId):
    skList = selectQuery(selectSocketList(None,'Y',pkgId))
    for index, sk in enumerate(skList):
        # 해더정보 처리
        hdList = selectQuery(selectTbSkMsgHdDt().format(sk.get('HD_ID')))
        if (len(hdList) > 0):
            sk[sk['HD_ID']] = hdList
            hdlen = selectQuery(selectHdLen().format(sk.get('HD_ID')))
            sk['HD_LEN'] = hdlen[0].get('HD_LEN')
        else:
            sk['HD_LEN'] = 0

        if sk['SK_GROUP'] is not None:
            sk['BZ_EVENT_INFO'] = selectQuery(selectListTbSkBz().format(sk.get('SK_GROUP')))

    return skList


def getsocketBody():
    msgList = selectQuery(selectMsgBodyList())
    for index, msg in enumerate(msgList):
        dtvalList = selectQuery(selectTbSkMsgBodyDtAndVal().format(msg.get('MSG_ID')))
        msg[msg['MSG_ID']] = dtvalList
        dtLen = selectQuery(selectMsgLen().format(msg.get('MSG_ID')))
        if (len(dtLen) > 0):
            msg['MSG_LEN'] = dtLen[0].get('MSG_LEN')
        else:
            msg['MSG_LEN'] = 0
    return msgList


def getsokcetIn(pkgId):
    return selectQuery(selectSkInList(None,pkgId))

def getsokcetOut():
    return selectQuery(selectSkOutList())


def getsokcetSch():
    return selectQuery(selectListTbSkSch())


# def getsokcetBz():
#     return selectQuery(selectListTbSkBz())

def selectQuery(queryString):
    c = dbInstance.cursor()
    c.execute(queryString)
    rows = c.fetchall()
    # 열 이름 가져오기
    column_names = [description[0] for description in c.description]
    # 데이터를 JSON 형식으로 변환
    json_data = []
    for row in rows:
        json_data.append(dict(zip(column_names, row)))
    return json_data

def queryExecute(queryString):
    c = dbInstance.cursor()
    c.execute(queryString)
    c.execute('COMMIT;')



logger.info(f'비즈니스 컨트롤러 초기화 ------------------')
handler = SendHandler(sokcetList, socketBody, sokcetBz, sokcetIn)
systemGlobals['TestController'] = TestController(handler)
socketBody = getsocketBody()
logger.info(f'------------------- ------------------')

def initPkgData(pkgId):
    logger.info(f'-----------RUN PKG_ID = {pkgId}---------------')
    # 가비지 컬렉션 강제 실행 (선택 사항)
    gc.collect()
    for idex, item in enumerate(systemGlobals['sokcetList']):
        del item

    systemGlobals['sokcetList'] = None
    sokcetList = getsokcetList(pkgId)
    # sokcetBz = getsokcetBz()
    systemGlobals['sokcetIn'] = None
    sokcetIn = getsokcetIn(pkgId)
    sokcetSch = getsokcetSch()

    logger.info(f'sokcetList size : {len(sokcetList)}')
    logger.info(f'sokcetSch size : {len(sokcetSch)}')
    logger.info(f'socketBody size : {len(socketBody)}')
    logger.info(f'sokcetBz size : {len(sokcetBz)}')
    logger.info(f'sokcetIn size : {len(sokcetIn)}')
    logger.info(f'sokcetSch size : {len(sokcetSch)}')


    # 비즈니스로직 처리 컨트롤러 지정

    systemGlobals['sokcetList'] = sokcetList
    systemGlobals['socketBody'] = socketBody
    systemGlobals['sokcetIn'] = sokcetIn
    logger.info(f'---------------------------------------')




