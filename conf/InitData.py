from conf.logconfig import logger
from conf.sql.SystemQueryString import *
from src.controller.TestController import TestController
import sys,os ,json, sqlite3


dbUrl=''
dbUser=''
dbPwd=''

# 파일 경로
file_path = "./config.json"
# 파일이 없을 경우에만 JSON 파일 생성
if not os.path.exists(file_path):
    with open(file_path, "w") as file:
        json.dump({}, file)
        print(f"{file_path} 파일이 생성되었습니다.")
        logger.info("config file created")
else:
    logger.info("config file is already exits")

with open(file_path, 'r') as f:
    data = json.load(f)




dbInstance = sqlite3.connect('core.db') # socket system DB
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
sokcetBz = []
sokcetIn = []
sokcetInToOut = []
sokcetOut = []
sokcetSub = []
sokcetSch = []
mainLayout = None
mainInstance = None
runChannels = [] # client,server 통합 접속된 채널 리스트

logger.info(f'비즈니스 컨트롤러 초기화 ------------------')
systemGlobals = globals()
systemGlobals['TestController'] = TestController()
logger.info(f'------------------- ------------------')


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


relative_path = resource_path('')
logger.info(f'relative_path :: {relative_path}')


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


def getsokcetSch(pkgId):
    return selectQuery(selectListTbSkSch(pkgId))


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




def initPkgData(pkgId):
    logger.info(f'-----------RUN PKG_ID = {pkgId}---------------')
    systemGlobals['sokcetList'] = None
    # systemGlobals['TestController'] = None
    systemGlobals['sokcetIn'] = None

    sokcetList = getsokcetList(pkgId)
    sokcetIn = getsokcetIn(pkgId)
    sokcetSch = getsokcetSch(pkgId)
    socketBody = getsocketBody()

    # logger.info(f'비즈니스 컨트롤러 초기화 ------------------')
    # handler = SendHandler(sokcetList, socketBody, sokcetBz, sokcetIn)
    # systemGlobals['TestController'] = TestController(handler)
    # logger.info(f'------------------- ------------------')

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




