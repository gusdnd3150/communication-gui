from conf.logconfig import logger
from conf.sql.SystemQueryString import *
from src.controller.TestController import TestController
from src.controller.SchController import SchController
from src.controller.AtlasCopco import AtlasCopco

from src.protocols.SendHandler import SendHandler
import sys,os ,json, sqlite3, importlib, traceback
import inspect
from src.utils.ExcelUtils import ExcelUtils
from conf.DbHandler import Dbhandler

dbHandler = None


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
    useYn = data.get('USE_YN')
    if useYn == 'Y':
        dbHandler = Dbhandler(data)

print("Current Working Directory:", os.getcwd())


dbInstance = sqlite3.connect('core.db') # socket system DB
useYnCombo = ['Y','N']
skTypeCombo = ['TCP','UDP','WEBSK']
skConnCombo = ['SERVER','CLIENT']
skClientCombo = ['KEEP','EVENT']
jobTypeCombo = ['SEC','MIN','HOUR','CRON']
eventTypeCombo = ['ACTIVE','KEEP','IDLE_READ','INACTIVE']
hdCombo = ['LENGTH_STR_8B','LENGTH_STR_20B','LENGTH_20B','COPCO_STR_20B','FREE','JSON']
#
# plcMakerCombo = ['Mitsubishi','Simens']
plcMakerCombo = ['LS']
# commTyCombo = ['binary','ascii']
commTyCombo = ['binary']
slotCombo = ['0','1','2','3']
rackCombo = ['0','1','2','3']

lsCpuTyCombo = ['XGT']
simenCpuTyCombo = ['S7300','S7400','S71200','S71500']
simenProtocolCombo = ['S7']
mitsuCpuTyCombo = ['FX3U','FX3G','QnA','QnC','L']
mitsuProtocolCombo = ['MC']


sokcetList = []
plcList = []
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
mainLayout = None   # GUI ui
mainInstance = None # GUI 메인 인스턴스
runChannels = [] # 접속중인 채널 리스트

logger.info(f'Global Controller Instance Generate! ------------------')
systemGlobals = globals()
systemGlobals['TestController'] = TestController()
systemGlobals['SchController'] = SchController()
systemGlobals['AtlasCopco'] = AtlasCopco()
logger.info(f'------------------- ------------------')

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


relative_path = resource_path('')
logger.info(f'relative_path :: {relative_path}')



def setCombos():
    data = {}
    data['PKG_LIST'] = selectQuery(selectPkgCombo())

    return data


def getPlcList(pkgId):
    list = selectQuery(selectPlcList(None, 'Y', pkgId))
    for plc in list:
        pkgId, plcId = plc['PKG_ID'], plc['PLC_ID']
        plc['ADDR_LIST'] = selectQuery(selectPlcAddrList(pkgId,plcId,'Y'))
    return list


def getsokcetList(pkgId):
    skList = selectQuery(selectInitSocketList(None,'Y',pkgId))
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

def getheaderCombo():
    headers = selectQuery(selectHeaderList())

    for index, sk in enumerate(headers):
        logger.info(f'{sk}')

    return ['1']



def getsokcetIn(pkgId):
    return selectQuery(selectSkInList(None,pkgId))

def getsokcetOut():
    return selectQuery(selectSkOutList())


def getsokcetSch(pkgId):
    return selectQuery(selectListTbSkSch(pkgId))

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

def selectQueryAsInt(queryString):
    c = dbInstance.cursor()
    c.execute(queryString)
    rslt = c.fetchall()
    # 열 이름 가져오기
    return rslt[0][0]


def insertConnHis(skId, chInfo, flag):
    try:
        cnt = selectQueryAsInt('SELECT COUNT(1) FROM TB_SK_PKG_SK_CONN_HIS')
        if cnt < 100: # 100 row만 관리
            queryExecute(f"INSERT INTO TB_SK_PKG_SK_CONN_HIS(	SK_ID	,CONN_IP	,CONN_STAT	,REG_DT)VALUES(	'{skId}','{str(chInfo)}','{flag}'	,datetime('now','localtime'));")
    except:
        traceback.print_exc()


def queryExecute(queryString):
    c = dbInstance.cursor()
    c.execute(queryString)
    c.execute('COMMIT;')

def initPkgData(pkgId):
    logger.info(f'-----------RUN PKG_ID = {pkgId}---------------')
    systemGlobals['sokcetList'] = None
    systemGlobals['sokcetSch'] = None
    systemGlobals['sokcetIn'] = None
    systemGlobals['plcList'] = None

    plcList = getPlcList(pkgId)
    sokcetList = getsokcetList(pkgId)
    sokcetIn = getsokcetIn(pkgId)
    sokcetSch = getsokcetSch(pkgId)
    socketBody = getsocketBody()

    # logger.info(f'비즈니스 컨트롤러 초기화 ------------------')
    # handler = SendHandler(sokcetList, socketBody, sokcetBz, sokcetIn)
    # systemGlobals['TestController'] = TestController(handler)
    # logger.info(f'------------------- ------------------')

    logger.info(f'plcList size : {len(plcList)}')
    logger.info(f'sokcetList size : {len(sokcetList)}')
    logger.info(f'sokcetSch size : {len(sokcetSch)}')
    logger.info(f'socketBody size : {len(socketBody)}')
    logger.info(f'sokcetBz size : {len(sokcetBz)}')
    logger.info(f'sokcetIn size : {len(sokcetIn)}')

    # 비즈니스로직 처리 컨트롤러 지정
    systemGlobals['sokcetList'] = sokcetList
    systemGlobals['plcList'] = plcList
    systemGlobals['socketBody'] = socketBody
    systemGlobals['sokcetIn'] = sokcetIn
    systemGlobals['sokcetSch'] = sokcetSch
    logger.info(f'---------------------------------------')


def projectPath():
    return os.path.dirname(os.path.abspath(__file__))


# 특정 경로의 py 파일을 동적으로 인스턴스화 시킨다
def load_all_classes_from_directory(directory_path: str):
    instances = []
    logger.info(f'directory_path :{directory_path}')
    for file_name in os.listdir(directory_path):
        try:
            if file_name.endswith('.py') and file_name != os.path.basename(__file__):
                file_path = os.path.join(directory_path, file_name)
                module_name = os.path.splitext(file_name)[0]

                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)

                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and obj.__module__ == module_name:
                        instances.append(obj(logger, SendHandler()))
        except Exception as e:
            logger.error(f'load_all_classes_from_directory error : {traceback.format_exc()}')

    return instances


if os.path.exists('./tempBz/'):
    classes = load_all_classes_from_directory('./tempBz/')
    for index, classInstance in enumerate(classes):
        systemGlobals[classInstance.classNm] = classInstance

