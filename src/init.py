import sys
import traceback
import os
from PySide6.QtWidgets import QMainWindow,  QTableWidgetItem, QHeaderView, QMessageBox
from PySide6.QtGui import QColor, QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt
from src.protocols.tcp.ServerThread2 import ServerThread2
from src.protocols.tcp.ClientThread2 import ClientThread2
program_path = sys.argv[0]
import logging
program_directory = os.path.dirname(program_path)
from src.component.settings.Settings import Settings
from src.component.handler.Handler import Handler
from src.component.log.Log import Log
import conf.skModule as moduleData
from conf.logconfig import logger
from src.protocols.udp.ServerUdpThread import ServerUdpThread
from src.protocols.udp.ClientUdpThread import ClientUdpThread
from src.protocols.websk.WebSkServerThread import WebSkServerThread
from src.protocols.websk.WebSkClientThread import WebSkClientThread

from src.protocols.sch.Schedule import Schedule
from src.protocols.bluetooth.BlueToothServerThread import BlueToothServerThread
from src.protocols.bluetooth.BlueToothClientThread import BlueToothClientThread

import time
from datetime import datetime
from ui.ui_main import Ui_MainWindow


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
    isRunSk = False
    treeModel = None
    root_node = None

    def __init__(self):
        super(InitClass, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        logger.info('application start')
        self.setWindowTitle('application')
        self.ui.btn_settings.clicked.connect(self.open_settings)
        # self.ui.btn_settings.setIcon()

        self.ui.btn_start.clicked.connect(self.start_sk)
        self.ui.btn_stop.clicked.connect(self.stop_sk)
        self.ui.btn_handler.clicked.connect(self.open_handler)
        self.ui.btn_show_log.clicked.connect(self.open_logger)

        moduleData.mainLayout = self.ui
        moduleData.mainInstance = self
        self.bindData()
        self.setGrid()

        # 설정팝업
        self.popup = Settings(self.initData)
        self.handlPop = Handler(self.initData)
        self.logPop = Log(self.initData)


    def closeEvent(self, event):
        # X 버튼을 눌렀을 때의 이벤트 감지
        reply = QMessageBox.question(self, '창 닫기',
                                     '정말로 닫으시겠습니까?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.stop_sk()
            self.popup.close()
            self.handlPop.close()
            event.accept()  # 창을 닫음
        else:
            event.ignore()  # 창 닫기 무시
    def bindData(self):
        for i in range(0, len(pkgCombo)):
            self.ui.combo_pkg.addItem(pkgCombo[i])

    def stop_sk(self):
        try:

            if self.isRunSk:
                reply = QMessageBox.question(self, '프로세스 중지',
                                             '소켓을 종료 하시겠습니까?',
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply != QMessageBox.Yes:
                    return
            logger.info(f'Stop Run Sockets')


            for i, item in enumerate(moduleData.sokcetList):
                if item['SK_CLIENT_TYPE'] == 'EVENT':
                    continue
                try:
                    runThread = item['SK_THREAD']
                    runThread.stop()
                    runThread.join()
                    item['SK_THREAD'] = None
                except:
                    logger.error(f'stop_sk exception {item["SK_ID"]}')


            for i, item in enumerate(moduleData.sokcetSch):
                runThread = item['SK_THREAD']
                runThread.stop()
                # runThread.join()
                item['SK_THREAD'] = None

            self.ui.combo_pkg.setDisabled(False)
            self.ui.btn_start.setDisabled(False)

            self.isRunSk = False
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

        pkg = self.ui.combo_pkg.currentText()
        # 기준정보 로드
        moduleData.initPkgData(pkg)


        self.handlPop.ui.combo_sk_list.clear()
        self.ui.combo_pkg.setDisabled(True)
        self.ui.btn_start.setDisabled(True)

        try:
            logger.info(f' Run Cnt : {len(moduleData.sokcetList)}')
            for i , item in enumerate(moduleData.sokcetList):
                threadInfo = None
                skTy = item['SK_TYPE']
                skConTy = item['SK_CONN_TYPE']
                skClientTy = item['SK_CLIENT_TYPE']


                if(skTy == 'TCP'):
                    if(skConTy=='SERVER'):
                        # threadInfo = ServerThread(item)
                        threadInfo = ServerThread2(item)
                    elif (skConTy == 'CLIENT'):
                        if skClientTy == 'KEEP':
                            # threadInfo = ClientThread(item)
                            threadInfo = ClientThread2(item)

                elif (skTy == 'UDP'):
                    if (skConTy == 'SERVER'):
                        threadInfo = ServerUdpThread(item)
                    elif (skConTy == 'CLIENT'):
                        threadInfo = ClientUdpThread(item)

                elif (skTy == 'WEBSK'):
                    if (skConTy == 'SERVER'):
                        threadInfo = WebSkServerThread(item)
                    elif (skConTy == 'CLIENT'):
                        threadInfo = WebSkClientThread(item)

                elif (skTy == 'BLUETOOTH'):
                    if (skConTy == 'SERVER'):
                        threadInfo = BlueToothServerThread(item)
                    elif (skConTy == 'CLIENT'):
                        threadInfo = BlueToothClientThread(item)

                else:
                    logger.info(f'None condition')
                    continue

                item['SK_THREAD'] = threadInfo
                self.handlPop.ui.combo_sk_list.addItem(item['SK_ID'])

                # KEEP일때만 실행 EVENT 방식일땐 상황에 맞춰 실행
                if skClientTy == 'KEEP':
                    threadInfo.daemon = True
                    threadInfo.start()

            
            for index, sch in enumerate(moduleData.sokcetSch):
                schThread = Schedule(sch)
                schThread.damon = True
                schThread.start()
                sch['SK_THREAD'] = schThread

            self.isRunSk = True
        except Exception as e:
            traceback.print_exc()
            logger.info(f'Init.start_sk() Exception :: {traceback.format_exc()}')
            # traceback.print_exc()


    def setGrid(self):
        self.ui.list_run_server.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.list_run_server.verticalHeader().setVisible(False)  # 행 번호 헤더 숨기기
        # self.ui.list_run_server.horizontalHeader().setVisible(False)  # 열 번호 헤더 숨기기
        self.ui.list_run_server.setRowCount(0)  # Table의 행을 설정, list의 길이
        self.ui.list_run_server.setColumnCount(9)
        self.ui.list_run_server.setHorizontalHeaderLabels(
            [
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

        self.ui.list_run_client.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.list_run_client.verticalHeader().setVisible(False)
        self.ui.list_run_client.setRowCount(0)  # Table의 행을 설정, list의 길이
        self.ui.list_run_client.setColumnCount(9)

        self.ui.list_run_client.setHorizontalHeaderLabels(
            [
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


        # self.ui.list_conn
        self.treeModel = QStandardItemModel()
        # self.treeModel.setHorizontalHeaderLabels(["Item", "Description"])
        self.treeModel.setHorizontalHeaderLabels(["Item"])
        self.root_node = self.treeModel.invisibleRootItem()





    def addServerRow(self, initData):
        try:
            # logger.info(f'addTableRow / initData: {initData}')
            row_count = self.ui.list_run_server.rowCount()
            self.ui.list_run_server.insertRow(row_count)
            # 예제 데이터를 추가
            self.ui.list_run_server.setItem(row_count, 0, QTableWidgetItem(initData['SK_ID']))
            self.ui.list_run_server.setItem(row_count, 1, QTableWidgetItem(initData['SK_GROUP']))
            self.ui.list_run_server.setItem(row_count, 2, QTableWidgetItem(initData['SK_TYPE']))
            self.ui.list_run_server.setItem(row_count, 3, QTableWidgetItem(initData['SK_CLIENT_TYPE']))
            self.ui.list_run_server.setItem(row_count, 4, QTableWidgetItem(initData['HD_ID']))
            # self.ui.list_run_server.setItem(row_count, 6, QTableWidgetItem(str(initData['SK_IP'])))
            item_sk_group = QTableWidgetItem(str(initData['SK_IP']))
            item_sk_group.setForeground(QColor('blue'))
            self.ui.list_run_server.setItem(row_count, 5, item_sk_group)

            self.ui.list_run_server.setItem(row_count, 6, QTableWidgetItem(str(initData['SK_PORT'])))
            self.ui.list_run_server.setItem(row_count, 7, QTableWidgetItem(str(initData['SK_DELIMIT_TYPE'])))
            self.ui.list_run_server.setItem(row_count, 8, QTableWidgetItem(str(initData['MAX_LENGTH'])))


        except Exception as e:
            logger.info(f'addTableRow exception : {e}')




    def addClientRow(self, initData):
        try:
            # logger.info(f'addTableRow / initData: {initData}')
            row_count = self.ui.list_run_client.rowCount()
            self.ui.list_run_client.insertRow(row_count)
            # 예제 데이터를 추가
            self.ui.list_run_client.setItem(row_count, 0, QTableWidgetItem(initData['SK_ID']))
            self.ui.list_run_client.setItem(row_count, 1, QTableWidgetItem(initData['SK_GROUP']))
            self.ui.list_run_client.setItem(row_count, 2, QTableWidgetItem(initData['SK_TYPE']))
            self.ui.list_run_client.setItem(row_count, 3, QTableWidgetItem(initData['SK_CLIENT_TYPE']))
            self.ui.list_run_client.setItem(row_count, 4, QTableWidgetItem(initData['HD_ID']))
            # self.ui.list_run_client.setItem(row_count, 6, QTableWidgetItem(str(initData['SK_IP'])))
            # self.ui.list_run_server.setItem(row_count, 6, QTableWidgetItem(str(initData['SK_IP'])))
            item_sk_group = QTableWidgetItem(str(initData['SK_IP']))
            item_sk_group.setForeground(QColor('#d87a7a'))
            self.ui.list_run_client.setItem(row_count, 5, item_sk_group)
            self.ui.list_run_client.setItem(row_count, 6, QTableWidgetItem(str(initData['SK_PORT'])))
            self.ui.list_run_client.setItem(row_count, 7, QTableWidgetItem(str(initData['SK_DELIMIT_TYPE'])))
            self.ui.list_run_client.setItem(row_count, 8, QTableWidgetItem(str(initData['MAX_LENGTH'])))


        except Exception as e:
            logger.info(f'addTableRow exception : {e}')
    def modServerRow(self,skId ,colunmNm, data):
        try:
            items = self.ui.list_run_server.findItems(skId, Qt.MatchExactly)
            index = self.get_column_index_by_name('server',colunmNm)
            if items:
                for item in items:
                    row = item.row()
                    # 특정 열(예: 열 1)을 수정
                    self.ui.list_run_server.setItem(row, index, QTableWidgetItem(data))
                    # self.ui.list_run_server.scrollToItem(item)  # 수정된 행으로 스크롤
                    # self.ui.list_run_server.setCurrentItem(item)  # 수정된 항목을 선택
        except Exception:
            logger.error(f'modServerRow exception : {traceback.format_exc()}')

    def modClientRow(self,skId ,colunmNm, data):
        try:
            items = self.ui.list_run_client.findItems(skId, Qt.MatchExactly)
            index = self.get_column_index_by_name('client',colunmNm)
            if items:
                for item in items:
                    row = item.row()
                    # 특정 열(예: 열 1)을 수정
                    self.ui.list_run_client.setItem(row, index, QTableWidgetItem(data))
                    # self.ui.list_run_server.scrollToItem(item)  # 수정된 행으로 스크롤
                    # self.ui.list_run_server.setCurrentItem(item)  # 수정된 항목을 선택
        except Exception:
            logger.error(f'modClientRow exception : {traceback.format_exc()}')


    def deleteTableRow(self, skId, target):
        try:
            if target == 'list_run_client':
                items = self.ui.list_run_client.findItems(skId, Qt.MatchExactly)
                for item in items:
                    self.ui.list_run_client.removeRow(item.row())
            elif target == 'list_run_server':
                items = self.ui.list_run_server.findItems(skId, Qt.MatchExactly)
                for item in items:
                    self.ui.list_run_server.removeRow(item.row())


        except Exception as e:
            logger.error(f'deleteTableRow exception : {traceback.format_exc()}')

    def get_column_index_by_name(self,target, column_name):
        headers = 0
        if target == 'server':
            headers = [self.ui.list_run_server.horizontalHeaderItem(i).text() for i in range(self.ui.list_run_server.columnCount())]
        else :
            headers = [self.ui.list_run_client.horizontalHeaderItem(i).text() for i in
                       range(self.ui.list_run_client.columnCount())]
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
    def open_logger(self):
        if self.logPop.isVisible():
            self.logPop.hide()
        else:
            self.logPop.show()


    def closeMain(self):
        logger.info(f'close ``````````````````````````')



    def updateConnList(self):
        try:
            self.treeModel.clear()  # 모델의 모든 항목 제거
            # self.treeModel.setHorizontalHeaderLabels(["SK_ID", "Description"])  # 헤더 다시 설정
            self.treeModel.setHorizontalHeaderLabels(["connection Info"])  # 헤더 다시 설정
            self.root_node = self.treeModel.invisibleRootItem()

            logger.info(f'updateConnList start')
            for index, item in enumerate(moduleData.sokcetList):
                skItem = QStandardItem( item['SK_ID'] )
                description_item = QStandardItem( item['SK_CONN_TYPE'])
                for skId, client, thread in moduleData.runChannels:
                    if skId == item['SK_ID']:
                        # skItem.appendRow([QStandardItem(str(client)), QStandardItem(str(thread))])
                        skItem.appendRow([QStandardItem(f'{str(client)} -- {thread}')])

                # 루트 노드에 부모 항목 추가 (여러 열)
                # self.root_node.appendRow([skItem, description_item])
                self.root_node.appendRow([skItem])
            self.ui.list_conn.setModel(self.treeModel)
            self.ui.list_conn.expandAll()

        except:
            logger.error(f'updateConnList exception: {traceback.format_exc()}')


    def insertLog(self, skId, bytes, flag):
        try:
            pass
            # if self.ui.chkbox_show_log.isChecked():
            #     logTm = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            #     self.ui.list_log.appendPlainText(f'SK_ID : {skId} [{logTm}] {flag} --- [{bytes.decode("ascii")}] \n')
        except:
            logger.error(f'insertLog exception: {traceback.format_exc()}')