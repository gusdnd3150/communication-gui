import sys
import traceback

import os

from src.protocols.tcp.ServerThread import ServerThread
from src.protocols.tcp.ClientThread import ClientThread
from src.protocols.tcp.ClientEventThread import ClientEventThread
import psutil
import time
from conf.InitData_n import systemGlobals

program_path = sys.argv[0]
program_directory = os.path.dirname(program_path)

from src.utils.Container import Container
from src.utils.InitData import InitData
from PySide6 import QtWidgets
from PySide6.QtUiTools import QUiLoader

from src.component.settings.Settings import Settings
from conf.logconfig import logger
from src.utils.SystemMonitor import SystemMonitor
from conf.InitData_n import systemGlobals

import threading

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

program_path = sys.argv[0]
program_directory = os.path.dirname(program_path)


# logger.info(resource_path('test.ui'))
# form = resource_path('test.ui')


pkgCombo = [
    'CORE'
    ,'TOOL'
    ,'MES'
]

# 네이밍
# 1. btn_?, popup_?, input_?,

class InitClass():

    mainLayOut = None
    popup = None # 설정 팝업
    saveSkWindow = None
    qLoader = None
    list_table = None
    initData = None # 초기데이터 초기화 클래스
    
    runSkList= [] #구동중인 소켓
    reactor = None
    def __init__(self):
        logger.info('init UI start')
        self.qLoader = QUiLoader()
        app = QtWidgets.QApplication(sys.argv)


        #메인창
        self.mainLayOut = self.qLoader.load(resource_path('main.ui'), None)
        self.mainLayOut.setWindowTitle('application')
        self.mainLayOut.btn_settings.clicked.connect(self.open_settings)
        self.mainLayOut.btn_start.clicked.connect(self.start_sk)
        self.mainLayOut.show()
        systemGlobals['mainLayout'] = self.mainLayOut

        self.bindData()

        # 설정팝업
        self.popup = Settings(self.initData)
        self.setEvent()
        self.setInitData()
        app.exec()


    def bindData(self):
        for i in range(0, len(pkgCombo)):
            self.mainLayOut.combo_pkg.addItem(pkgCombo[i])


    def start_sk(self):




        pkg = self.mainLayOut.combo_pkg.currentText()

        try:



            for i , item in enumerate(systemGlobals['sokcetList']):
                threadInfo = None
                skTy = item['SK_TYPE']
                skConTy = item['SK_CONN_TYPE']
                skClientTy = item['SK_CLIENT_TYPE']

                if(skTy == 'TCP'):
                    if(skConTy=='SERVER'):
                        threadInfo = ServerThread(item)
                    elif (skConTy == 'CLIENT'):
                        if skClientTy == 'KEEP':
                            threadInfo = ClientThread(item)
                        elif skClientTy == 'EVENT':
                            threadInfo = ClientEventThread(item)
                else:
                    logger.info('None Condition')
                    continue

                item['SK_THREAD'] = threadInfo

                # KEEP일때만 실행 EVENT 방식일땐 상황에 맞춰 실행
                if skClientTy == 'KEEP':
                    threadInfo.daemon = True
                    threadInfo.start()

            sysThread = SystemMonitor(self.mainLayOut)
            sysThread.daemon = True
            sysThread.start()
        except Exception as e:
            logger.info(f'Init.start_sk() Exception :: {e}')
            # traceback.print_exc()






    def setEvent(self):
        # self.popup
        # self.mainLayOut
        logger.info('tset')

        # list_table =

    def setInitData(self):
        logger.info('load Init Data')
        program_directory+'\json\*.json'



    def open_settings(self):
        logger.info('tesst')
        if self.popup.isVisible():
            # self.popup.instance.hide()
            self.popup.hide()
        else:
            # self.popup.instance.show()
            self.popup.show()


    def addTableRow(self, items):
        logger.info('test')
