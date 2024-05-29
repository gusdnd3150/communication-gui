import sys
import traceback

import os

from src.protocols.tcp.SocketServer import SocketServer
from src.protocols.tcp.SocketClient import SocketClient



program_path = sys.argv[0]
program_directory = os.path.dirname(program_path)

# from src.utils.Container import Container
from src.utils.InitData import InitData
from PySide6 import QtWidgets
from PySide6.QtUiTools import QUiLoader

from src.component.settings.Settings import Settings
from conf.logconfig import logger

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

program_path = sys.argv[0]
program_directory = os.path.dirname(program_path)


# logger.info(resource_path('test.ui'))
# form = resource_path('test.ui')


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

    def __init__(self):
        # container = Container()
        # initData = container.InitData_bean
        self.initData =InitData()
        self.initData.loadDb()

        logger.info('init UI start')
        self.qLoader = QUiLoader()
        app = QtWidgets.QApplication(sys.argv)

        #메인창
        self.mainLayOut = self.qLoader.load(resource_path('main.ui'), None)
        self.mainLayOut.setWindowTitle('application')
        self.mainLayOut.btn_settings.clicked.connect(self.open_settings)
        self.mainLayOut.btn_start.clicked.connect(self.start_sk)
        self.mainLayOut.show()

        # 설정팝업
        # self.popup = Settings(self.initData)
        self.setEvent()
        self.setInitData()
        app.exec()

    def start_sk(self):
        try:
            logger.info('socket List start')
            skList = self.initData.sokcetList
            for i , item in enumerate(skList):
                useYn = item['USE_YN']
                if(useYn =='Y'):
                    threadInfo = None

                    skTy = item['SK_TYPE']
                    skConTy = item['SK_CONN_TYPE']
                    skId = item['SK_ID']

                    if(skTy == 'TCP'):
                        if(skConTy=='SERVER'):
                            threadInfo = SocketServer(item)
                        elif (skConTy == 'CLIENT'):
                            threadInfo = SocketClient(item)



                    elif(skTy == 'UDP'):
                        if (skConTy == 'SERVER'):
                            threadInfo = SocketServer(item)
                        elif (skConTy == 'CLIENT'):
                            threadInfo = SocketClient(item)
                        # threadInfo.daemon = True
                        # threadInfo.start()

                    else:
                        logger.info('None Condition')

                    threadInfo.daemon = True
                    threadInfo.start()
                    # threadInfo.run()

                    # 구동 소켓 리스트 메모리 저장
                    self.runSkList.append(threadInfo)

        except :
            logger.info('exception')
            traceback.print_exception()
            # traceback.print_stack()


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
        if self.popup.instance.isVisible():
            self.popup.instance.hide()
        else:
            self.popup.instance.show()


    def addTableRow(self, items):
        logger.info('test')
