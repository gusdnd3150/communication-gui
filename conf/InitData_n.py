from conf.logconfig import logger
import sqlite3
from conf.QueryString import *



logger.info('DB connectiom with SqlLite')
dbInstance = sqlite3.connect('core.db')

def getsokcetList():
    skList = selectQuery(selectSocketList())
    for index, sk in enumerate(skList):
        hdList = selectQuery(selectTbSkMsgHdDt().format(sk.get('HD_ID')))
        if (len(hdList) > 0):
            sk[sk['HD_ID']] = hdList
            hdlen = selectQuery(selectHdLen().format(sk.get('HD_ID')))
            sk['HD_LEN'] = hdlen[0].get('HD_LEN')
        else:
            sk['HD_LEN'] = 0

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


def getsokcetIn():
    return selectQuery(selectSkInList())

def getsokcetOut():
    return selectQuery(selectSkOutList())


def getsokcetSch():
    return selectQuery(selectListTbSkSch())


def getsokcetBz():
    return selectQuery(selectListTbSkBz())

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


sokcetList = getsokcetList()
socketHd = []
socketHdDt = []
socketBody = getsocketBody()
socketBodyDt = []
socketVal = []
sokcetBz = getsokcetBz()
sokcetIn = getsokcetIn()
sokcetInToOut = []
sokcetOut = []
sokcetSub = []
sokcetSch = getsokcetSch()



logger.info(f'sokcetList size : {len(sokcetList)}')
logger.info(f'sokcetSch size : {len(sokcetSch)}')
logger.info(f'socketBody size : {len(socketBody)}')
logger.info(f'sokcetBz size : {len(sokcetBz)}')
logger.info(f'sokcetIn size : {len(sokcetIn)}')
logger.info(f'sokcetSch size : {len(sokcetSch)}')

