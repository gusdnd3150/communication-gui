
import sys
import os
import traceback
import json
from conf.logconfig import logger

program_path = sys.argv[0]
program_directory = os.path.dirname(program_path)

class InitData():

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


    def __init__(self):
        logger.info('InitData created')
        self.loadData()

    def loadData(self):
        self.sokcetList = self.loadJsonFile('TB_SK_PKG_SK')
        self.socketHd =  self.loadJsonFile('TB_SK_MSG_HD')
        self.socketHdDt =  self.loadJsonFile('TB_SK_MSG_HD_DT')
        self.socketBody =  self.loadJsonFile('TB_SK_MSG_BODY')
        self.socketBodyDt =  self.loadJsonFile('TB_SK_MSG_BODY_DT')
        self.socketVal =  self.loadJsonFile('TB_SK_MSG_VAL')
        self.sokcetBz =  self.loadJsonFile('TB_SK_PKG_SK_BZ')
        self.sokcetIn =  self.loadJsonFile('TB_SK_PKG_SK_IN')
        # sokcetInToOut =  self.loadJsonFile('TB_SK_PKG_SK')
        # sokcetOut = self.loadJsonFile('TB_SK_PKG_SK')
        # sokcetSub =  self.loadJsonFile('TB_SK_PKG_SK')
        self.sokcetSch =  self.loadJsonFile('TB_SK_PKG_SCH')

    def loadJsonFile(self, fileNm):
        try:
            logger.info(program_directory + '/json/' + fileNm + '.json')
            with open(program_directory + '/json/' + fileNm + '.json', 'rt', encoding='UTF8') as f:
                data = json.load(f)
                return data
        except:
            traceback.print_exc()
            return []

