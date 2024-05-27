
import sys
import os
import traceback
import json
from conf.logconfig import logger
import sqlite3
from src.utils.QueryString import *

program_path = sys.argv[0]
program_directory = os.path.dirname(program_path)

class InitData():

    dbInstance = None
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
    initYn = False

    def __init__(self):
        logger.info('InitData created')
        # self.loadData()
        self.loadDb()

    def loadData(self):
        print()
        # self.sokcetList = self.loadJsonFile('TB_SK_PKG_SK')
        # self.socketHd =  self.loadJsonFile('TB_SK_MSG_HD')
        # self.socketHdDt =  self.loadJsonFile('TB_SK_MSG_HD_DT')
        # self.socketBody =  self.loadJsonFile('TB_SK_MSG_BODY')
        # self.socketBodyDt =  self.loadJsonFile('TB_SK_MSG_BODY_DT')
        # self.socketVal =  self.loadJsonFile('TB_SK_MSG_VAL')
        # self.sokcetBz =  self.loadJsonFile('TB_SK_PKG_SK_BZ')
        # self.sokcetIn =  self.loadJsonFile('TB_SK_PKG_SK_IN')
        # # sokcetInToOut =  self.loadJsonFile('TB_SK_PKG_SK')
        # # sokcetOut = self.loadJsonFile('TB_SK_PKG_SK')
        # # sokcetSub =  self.loadJsonFile('TB_SK_PKG_SK')
        # self.sokcetSch =  self.loadJsonFile('TB_SK_PKG_SCH')



    def loadDb(self):
        try:
            logger.info('DB connectiom with SqlLite')
            self.dbInstance = sqlite3.connect('core.db')

            skList = self.selectQuery(selectSocketList())
            for index, sk in enumerate(skList):
                hdList =  self.selectQuery(selectTbSkMsgHdDt().format(sk.get('HD_ID')))
                if(len(hdList) > 0):
                    sk[sk['HD_ID']] = hdList
                    hdlen = self.selectQuery(selectHdLen().format(sk.get('HD_ID')))
                    sk['HD_LEN'] = hdlen[0].get('HD_LEN')

            msgList = self.selectQuery(selectMsgBodyList())
            for index, msg in enumerate(msgList):

                dtvalList = self.selectQuery(selectTbSkMsgBodyDtAndVal().format(msg.get('MSG_ID')))
                msg[msg['MSG_ID']] = dtvalList
                dtLen = self.selectQuery(selectMsgLen().format(msg.get('MSG_ID')))
                if(len(dtLen) > 0):
                    msg['MSG_LEN'] = dtLen[0].get('MSG_LEN')
                else:
                    msg['MSG_LEN'] = 0

                # logger.info(msg)
            inlist = self.selectQuery(selectSkInList())
            outlist = self.selectQuery(selectSkOutList())
            schlist = self.selectQuery(selectListTbSkSch())
            bzlist = self.selectQuery(selectListTbSkBz())

            logger.info("socketList.size():: " + str(len(skList)))
            logger.info("msgBodyList:: " + str(len(msgList)))
            logger.info("skInList:: " + str(len(inlist)))
            logger.info("skOutList:: " + str(len(outlist)))
            logger.info("skSchList:: " + str(len(schlist)))
            logger.info("skMqttTopicList:: " + str(len(bzlist)))

            self.sokcetList = skList
            self.socketBody = msgList
            self.sokcetIn = inlist
            self.sokcetOut = outlist
            self.sokcetSch = schlist
            self.sokcetBz = bzlist
        except:
            traceback.print_exc()


    def selectQuery(self, queryString):
        c = self.dbInstance.cursor()

        c.execute(queryString)
        rows = c.fetchall()

        # 열 이름 가져오기
        column_names = [description[0] for description in c.description]

        # 데이터를 JSON 형식으로 변환
        json_data = []
        for row in rows:
            json_data.append(dict(zip(column_names, row)))

        # JSON 포맷으로 변환된 데이터 출력
        # json_string = json.dumps(json_data, indent=4)
        # print(json_string)

        return json_data


    def loadJsonFile(self, fileNm):
        try:
            logger.info(program_directory + '/json/' + fileNm + '.json')
            with open(program_directory + '/json/' + fileNm + '.json', 'rt', encoding='UTF8') as f:
                data = json.load(f)
                return data
        except:
            traceback.print_exc()
            return []

