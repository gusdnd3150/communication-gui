import sys
import traceback
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt
from src.protocols.tcp.ServerThread import ServerThread
from src.protocols.tcp.ClientThread import ClientThread
from src.protocols.tcp.ClientEventThread import ClientEventThread
program_path = sys.argv[0]
import logging
program_directory = os.path.dirname(program_path)
from PySide6 import QtWidgets
from PySide6.QtUiTools import QUiLoader
from src.component.settings.Settings import Settings
from src.component.handler.Handler import Handler
import conf.skModule as moduleData
from conf.logconfig import logger
from src.protocols.udp.ServerUdpThread import ServerUdpThread
from src.protocols.udp.ClientUdpThread import ClientUdpThread
from src.protocols.websk.WebSkServerThread import WebSkServerThread
from src.protocols.sch.Schedule import Schedule


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

class InitClass(QMainWindow):

    mainLayOut = None
    popup = None # 설정 팝업
    saveSkWindow = None
    qLoader = None
    list_table = None
    initData = None # 초기데이터 초기화 클래스
    reactor = None
    handlPop =None

    def __init__(self):
        logger.info('init UI start')
        self.qLoader = QUiLoader()
        app = QtWidgets.QApplication(sys.argv)

        #메인창
        path = resource_path('main.ui')
        logger.info(f'path :: {path}')
        self.mainLayOut = self.qLoader.load(path, None)
        self.mainLayOut.setWindowTitle('application')
        self.mainLayOut.btn_settings.clicked.connect(self.open_settings)
        self.mainLayOut.btn_start.clicked.connect(self.start_sk)
        self.mainLayOut.btn_stop.clicked.connect(self.stop_sk)
        self.mainLayOut.btn_handler.clicked.connect(self.open_handler)

        self.mainLayOut.show()
        moduleData.mainLayout = self.mainLayOut
        moduleData.mainInstance = self
        super().__init__()

        # 설정팝업
        self.popup = Settings(self.initData)
        self.handlPop = Handler(self.initData)
        self.bindData()
        self.setGrid()
        self.setInitData()
        app.exec()

    def closeEvent(self, event):
        logger.info(f' 시스템 종료 ')

    def bindData(self):
        for i in range(0, len(pkgCombo)):
            self.mainLayOut.combo_pkg.addItem(pkgCombo[i])

    def stop_sk(self):
        try:
            logger.info(f'Stop Run Sockets')
            for i, item in enumerate(moduleData.sokcetList):
                if item['SK_CLIENT_TYPE'] == 'EVENT':
                    continue
                runThread = item['SK_THREAD']
                runThread.stop()
                runThread.join()
                item['SK_THREAD'] = None


            for i, item in enumerate(moduleData.sokcetSch):
                runThread = item['SK_THREAD']
                runThread.stop()
                item['SK_THREAD'] = None

            self.mainLayOut.list_conn.clearContents()
            self.mainLayOut.combo_pkg.setDisabled(False)
            self.mainLayOut.btn_start.setDisabled(False)
        except Exception as e:
            logger.error(f'stop_sk() exceptopn : {traceback.format_exc()}')

    def removeLogger(self,skId):
        logger = logging.getLogger(skId)
        # 모든 핸들러 제거
        handlers = logger.handlers[:]
        for handler in handlers:
            handler.close()
            logger.removeHandler(handler)
        # 로거 제거
        logging.getLogger(skId).handlers = []


    def start_sk(self):

        pkg = self.mainLayOut.combo_pkg.currentText()
        # 기준정보 로드
        moduleData.initPkgData(pkg)


        self.handlPop.ui.combo_sk_list.clear()
        self.mainLayOut.combo_pkg.setDisabled(True)
        self.mainLayOut.btn_start.setDisabled(True)

        try:
            logger.info(f' Run Cnt : {len(moduleData.sokcetList)}')
            for i , item in enumerate(moduleData.sokcetList):
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

                elif (skTy == 'UDP'):
                    if (skConTy == 'SERVER'):
                        threadInfo = ServerUdpThread(item)
                    elif (skConTy == 'CLIENT'):
                        threadInfo = ClientUdpThread(item)

                elif (skTy == 'WEBSK'):
                    if (skConTy == 'SERVER'):
                        threadInfo = WebSkServerThread(item)
                    elif (skConTy == 'CLIENT'):
                        threadInfo = ClientUdpThread(item)

                else:
                    logger.info(f'None condition')
                    continue

                item['SK_THREAD'] = threadInfo
                self.handlPop.ui.combo_sk_list.addItem(item['SK_ID'])

                # KEEP일때만 실행 EVENT 방식일땐 상황에 맞춰 실행
                if skClientTy == 'KEEP':
                    threadInfo.daemon = True
                    threadInfo.start()

            self.handlPop
            for index, sch in enumerate(moduleData.sokcetSch):
                schThread = Schedule(sch)
                schThread.damon = True
                schThread.start()
                sch['SK_THREAD'] = schThread

        except Exception as e:
            traceback.print_exc()
            logger.info(f'Init.start_sk() Exception :: {traceback.format_exc()}')
            # traceback.print_exc()


    def setGrid(self):

        self.mainLayOut.list_run_server.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.mainLayOut.list_run_server.verticalHeader().setVisible(False)  # 행 번호 헤더 숨기기
        # self.mainLayOut.list_run_server.horizontalHeader().setVisible(False)  # 열 번호 헤더 숨기기
        self.mainLayOut.list_run_server.setRowCount(0)  # Table의 행을 설정, list의 길이
        self.mainLayOut.list_run_server.setColumnCount(10)
        self.mainLayOut.list_run_server.setHorizontalHeaderLabels(
            [
            'CON_COUNT',
            'SK_ID',
            'SK_GROUP',
            'SK_TYPE',
            'SK_CLIENT_TYPE',
            'HD_ID',
            'SK_IP',
            'SK_PORT',
            'SK_DELIMIT_TYPE',
            'MAX_LENGTH'
             ]
        )

        self.mainLayOut.list_run_client.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.mainLayOut.list_run_client.verticalHeader().setVisible(False)
        self.mainLayOut.list_run_client.setRowCount(0)  # Table의 행을 설정, list의 길이
        self.mainLayOut.list_run_client.setColumnCount(10)
        self.mainLayOut.list_run_client.setHorizontalHeaderLabels(
            [
                'CON_COUNT',
                'SK_ID',
                'SK_GROUP',
                'SK_TYPE',
                'SK_CLIENT_TYPE',
                'HD_ID',
                'SK_IP',
                'SK_PORT',
                'SK_DELIMIT_TYPE',
                'MAX_LENGTH'
            ]
        )

        # self.mainLayOut.list_conn.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.mainLayOut.list_conn.verticalHeader().setVisible(False)
        self.mainLayOut.list_conn.setRowCount(0)  # Table의 행을 설정, list의 길이
        self.mainLayOut.list_conn.setColumnCount(2)
        self.mainLayOut.list_conn.setHorizontalHeaderLabels(
            [
                'SK_ID',
                'CONN_INFO',
            ]
        )
        header = self.mainLayOut.list_conn.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)



    def setInitData(self):
        logger.info('load Init Data')
        program_directory+'\json\*.json'


    def addServerRow(self, initData):
        try:
            # logger.info(f'addTableRow / initData: {initData}')
            row_count = self.mainLayOut.list_run_server.rowCount()
            self.mainLayOut.list_run_server.insertRow(row_count)
            # 예제 데이터를 추가
            self.mainLayOut.list_run_server.setItem(row_count, 0, QTableWidgetItem('0'))
            self.mainLayOut.list_run_server.setItem(row_count, 1, QTableWidgetItem(initData['SK_ID']))
            self.mainLayOut.list_run_server.setItem(row_count, 2, QTableWidgetItem(initData['SK_GROUP']))
            self.mainLayOut.list_run_server.setItem(row_count, 3, QTableWidgetItem(initData['SK_TYPE']))
            self.mainLayOut.list_run_server.setItem(row_count, 4, QTableWidgetItem(initData['SK_CLIENT_TYPE']))
            self.mainLayOut.list_run_server.setItem(row_count, 5, QTableWidgetItem(initData['HD_ID']))
            # self.mainLayOut.list_run_server.setItem(row_count, 6, QTableWidgetItem(str(initData['SK_IP'])))
            item_sk_group = QTableWidgetItem(str(initData['SK_IP']))
            item_sk_group.setForeground(QColor('#d87a7a'))
            self.mainLayOut.list_run_server.setItem(row_count, 6, item_sk_group)

            self.mainLayOut.list_run_server.setItem(row_count, 7, QTableWidgetItem(str(initData['SK_PORT'])))
            self.mainLayOut.list_run_server.setItem(row_count, 8, QTableWidgetItem(str(initData['SK_DELIMIT_TYPE'])))
            self.mainLayOut.list_run_server.setItem(row_count, 9, QTableWidgetItem(str(initData['MAX_LENGTH'])))


        except Exception as e:
            logger.info(f'addTableRow exception : {e}')


    def addConnRow(self, initData):
        try:
            # logger.info(f'addTableRow / initData: {initData}')
            row_count = self.mainLayOut.list_conn.rowCount()
            self.mainLayOut.list_conn.insertRow(row_count)
            # 예제 데이터를 추가
            self.mainLayOut.list_conn.setItem(row_count, 0, QTableWidgetItem(initData['SK_ID']))
            self.mainLayOut.list_conn.setItem(row_count, 1, QTableWidgetItem(str(initData['CONN_INFO'])))



        except Exception as e:
            logger.info(f'addTableRow exception : {e}')

    def addClientRow(self, initData):
        try:
            # logger.info(f'addTableRow / initData: {initData}')
            row_count = self.mainLayOut.list_run_client.rowCount()
            self.mainLayOut.list_run_client.insertRow(row_count)
            # 예제 데이터를 추가
            self.mainLayOut.list_run_client.setItem(row_count, 0, QTableWidgetItem('0'))
            self.mainLayOut.list_run_client.setItem(row_count, 1, QTableWidgetItem(initData['SK_ID']))
            self.mainLayOut.list_run_client.setItem(row_count, 2, QTableWidgetItem(initData['SK_GROUP']))
            self.mainLayOut.list_run_client.setItem(row_count, 3, QTableWidgetItem(initData['SK_TYPE']))
            self.mainLayOut.list_run_client.setItem(row_count, 4, QTableWidgetItem(initData['SK_CLIENT_TYPE']))
            self.mainLayOut.list_run_client.setItem(row_count, 5, QTableWidgetItem(initData['HD_ID']))
            # self.mainLayOut.list_run_client.setItem(row_count, 6, QTableWidgetItem(str(initData['SK_IP'])))
            # self.mainLayOut.list_run_server.setItem(row_count, 6, QTableWidgetItem(str(initData['SK_IP'])))
            item_sk_group = QTableWidgetItem(str(initData['SK_IP']))
            item_sk_group.setForeground(QColor('#d87a7a'))
            self.mainLayOut.list_run_client.setItem(row_count, 6, item_sk_group)
            self.mainLayOut.list_run_client.setItem(row_count, 7, QTableWidgetItem(str(initData['SK_PORT'])))
            self.mainLayOut.list_run_client.setItem(row_count, 8, QTableWidgetItem(str(initData['SK_DELIMIT_TYPE'])))
            self.mainLayOut.list_run_client.setItem(row_count, 9, QTableWidgetItem(str(initData['MAX_LENGTH'])))


        except Exception as e:
            logger.info(f'addTableRow exception : {e}')
    def modServerRow(self,skId ,colunmNm, data):
        try:
            items = self.mainLayOut.list_run_server.findItems(skId, Qt.MatchExactly)
            index = self.get_column_index_by_name('server',colunmNm)
            if items:
                for item in items:
                    row = item.row()
                    # 특정 열(예: 열 1)을 수정
                    self.mainLayOut.list_run_server.setItem(row, index, QTableWidgetItem(data))
                    # self.mainLayOut.list_run_server.scrollToItem(item)  # 수정된 행으로 스크롤
                    # self.mainLayOut.list_run_server.setCurrentItem(item)  # 수정된 항목을 선택
        except Exception:
            logger.error(f'modServerRow exception : {traceback.format_exc()}')

    def modClientRow(self,skId ,colunmNm, data):
        try:
            items = self.mainLayOut.list_run_client.findItems(skId, Qt.MatchExactly)
            index = self.get_column_index_by_name('client',colunmNm)
            if items:
                for item in items:
                    row = item.row()
                    # 특정 열(예: 열 1)을 수정
                    self.mainLayOut.list_run_client.setItem(row, index, QTableWidgetItem(data))
                    # self.mainLayOut.list_run_server.scrollToItem(item)  # 수정된 행으로 스크롤
                    # self.mainLayOut.list_run_server.setCurrentItem(item)  # 수정된 항목을 선택
        except Exception:
            logger.error(f'modClientRow exception : {traceback.format_exc()}')


    def deleteTableRow(self, skId, target):
        try:
            if target == 'list_run_client':
                items = self.mainLayOut.list_run_client.findItems(skId, Qt.MatchExactly)
                for item in items:
                    self.mainLayOut.list_run_client.removeRow(item.row())
            elif target == 'list_run_server':
                items = self.mainLayOut.list_run_server.findItems(skId, Qt.MatchExactly)
                for item in items:
                    self.mainLayOut.list_run_server.removeRow(item.row())
            elif target == 'list_conn':
                items = self.mainLayOut.list_conn.findItems(skId, Qt.MatchExactly)
                for item in items:
                    self.mainLayOut.list_conn.removeRow(item.row())


        except Exception as e:
            logger.error(f'deleteTableRow exception : {traceback.format_exc()}')

    def get_column_index_by_name(self,target, column_name):
        headers = 0
        if target == 'server':
            headers = [self.mainLayOut.list_run_server.horizontalHeaderItem(i).text() for i in range(self.mainLayOut.list_run_server.columnCount())]
        else :
            headers = [self.mainLayOut.list_run_client.horizontalHeaderItem(i).text() for i in
                       range(self.mainLayOut.list_run_client.columnCount())]
        try:
            return headers.index(column_name)
        except ValueError:
            return -1


    def open_settings(self):
        if self.popup.isVisible():
            # self.popup.instance.hide()
            self.popup.hide()
        else:
            # self.popup.instance.show()
            self.popup.show()

    def open_handler(self):
        if self.handlPop.isVisible():
            self.handlPop.hide()
        else:
            self.handlPop.show()

