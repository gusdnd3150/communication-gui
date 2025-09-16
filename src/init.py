import os
import sys
import traceback
from PySide6.QtCore import Slot, Qt
from PySide6.QtGui import QColor, QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView, QMessageBox

from src.component.sql.SqlHandler import SqlHandler
from src.protocols.plc.PlcMisubisiThread import PlcMisubisiThread
from src.protocols.plc.PlcSimensThread import PlcSimensThread
from src.protocols.tcp.ClientThread import ClientThread
from src.protocols.tcp.ServerThread import ServerThread
from src.thread.MsgHandler import MsgHandler
program_path = sys.argv[0]
import logging
program_directory = os.path.dirname(program_path)
from src.component.settings.Settings import Settings
from src.component.handler.Handler import Handler
import conf.skModule as moduleData
from conf.logconfig import logger
from src.protocols.udp.ServerUdpThread import ServerUdpThread
from src.protocols.udp.ClientUdpThread import ClientUdpThread
from src.protocols.websk.WebSkServerThread import WebSkServerThread
from src.protocols.websk.WebSkClientThread import WebSkClientThread
from src.protocols.sch.Schedule import Schedule
from src.protocols.bluetooth.BlueToothServerThread import BlueToothServerThread
from src.protocols.bluetooth.BlueToothClientThread import BlueToothClientThread
from src.thread.WorkThread import WorkThread
from src.thread.LogThread import LogThread
from ui.ui_main_new import Ui_MainWindow


from src.component.direct.Direct import Direct
from src.component.utility.Utility import Utility
from src.protocols.http.HttpServerThread import  HttpServerThread


# 네이밍
# 1. btn_?, popup_?, input_?,

class InitClass(QMainWindow):

    mainLayOut = None
    popup = None # 설정 팝업
    plc_popup = None # 설정 팝업
    saveSkWindow = None
    qLoader = None
    list_table = None
    initData = None # 초기데이터 초기화 클래스
    reactor = None
    handlPop =None
    utilityPop =None
    isRunSk = False
    treeModel = None
    root_node = None
    workThread = None # 실시간성 GUI 수정작업을 스레드를 통해 진행
    logThread = None
    mainLoop = None
    directPop =None
    msgHandler= None
    sqlHandler = None


    def __init__(self):
        super(InitClass, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        logger.info('application start')
        self.setWindowTitle('application (made by KHW)')

        # thread
        self.workThread = WorkThread()
        self.workThread.updateConnList.connect(self.workUpdateConnList)
        self.logThread = LogThread()
        self.logThread.updateLog.connect(self.insertLog)

        # button
        self.ui.btn_start.clicked.connect(self.start_sk)  # 시작버튼
        self.ui.btn_stop.clicked.connect(self.stop_sk)   # 종료버튼
        self.ui.log_btn_clear.clicked.connect(self.clickClear)
        # self.ui.btn_settings.clicked.connect(self.open_settings)
        # self.ui.btn_handler.clicked.connect(self.open_handler)
        # self.ui.btn_show_log.clicked.connect(self.open_logger)

        self.ui.action_util.triggered.connect(self.open_util) # 유틸
        self.ui.actionPlc_settings.triggered.connect(self.open_plc_settings) # 유틸
        self.ui.action_settings.triggered.connect(self.open_settings)  # 설정 오픈
        self.ui.action_test.triggered.connect(self.open_handler)  # 핸들러 오픈
        self.ui.actionOpen_log_folder.triggered.connect(self.openFolder) # 폴더 오픈
        self.ui.action_dirMessage.triggered.connect(self.open_direct)

        moduleData.mainLayout = self.ui
        moduleData.mainInstance = self

        self.msgHandler = MsgHandler(self.ui)
        self.bindData()
        self.setGrid()

        # 설정팝업
        self.popup = Settings(self.initData)
        self.plc_popup = Settings(self.initData)
        self.handlPop = Handler(self.initData)
        self.utilityPop = Utility(self.initData)
        self.directPop = Direct(self.initData)
        self.sqlHandler = SqlHandler(self.initData)
        # self.logPop = Log(self.initData)





    def updateConnList(self):
        try:
            self.workThread.start()
        except:
            traceback.print_exception()


    def closeEvent(self, event):
        # X 버튼을 눌렀을 때의 이벤트 감지
        reply = QMessageBox.question(self, '창 닫기',
                                     '정말로 닫으시겠습니까?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.stop_sk()
            self.popup.close()
            self.handlPop.close()
            self.utilityPop.close()

            event.accept()  # 창을 닫음
        else:
            event.ignore()  # 창 닫기 무시


    def bindData(self):
        list = moduleData.setCombos()
        logger.info(f'combo init :: {list}')
        for comKey in list.keys():
            if comKey == 'PKG_LIST':
                for item in list[comKey]:
                    self.ui.combo_pkg.addItem(item['PKG_ID'])

        # for i in range(0, len(pkgCombo)):
        #     self.ui.combo_pkg.addItem(pkgCombo[i])

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

            for i, item in enumerate(moduleData.plcList):
                thread = item['PLC_THREAD']
                if thread is not None:
                    try:
                        thread.stop()
                        thread.join()
                        item['PLC_THREAD'] = None
                    except:
                        logger.error(f'stop_sk exception {item["PLC_ID"]}')

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
        self.directPop.ui.dir_sk.clear()
        self.ui.main_combo_sk_list.clear()
        self.ui.combo_pkg.setDisabled(True)
        self.ui.btn_start.setDisabled(True)
        
        try:

            logger.info(f'start_sk() PLC Run Cnt : {moduleData.plcList}')
            for i, item in enumerate(moduleData.plcList):
                threadPlcInfo = None
                if item['PLC_MAKER'] == 'Simens':
                    threadPlcInfo = PlcSimensThread(item)
                elif item['PLC_MAKER'] == 'Misubisi':
                    threadPlcInfo = PlcMisubisiThread(item)

                if threadPlcInfo is not None:
                    threadPlcInfo.daemon = True
                    threadPlcInfo.start()
                    item['PLC_THREAD'] = threadPlcInfo


            logger.info(f'start_sk() Socket Run Cnt : {len(moduleData.sokcetList)}')
            for i , item in enumerate(moduleData.sokcetList):
                threadInfo = None
                skTy = item['SK_TYPE']
                skConTy = item['SK_CONN_TYPE']
                skClientTy = item['SK_CLIENT_TYPE']


                if(skTy == 'TCP'):
                    if(skConTy=='SERVER'):
                        # threadInfo = ServerThread(item)
                        threadInfo = ServerThread(item)
                    elif (skConTy == 'CLIENT'):
                        if skClientTy == 'KEEP':
                            # threadInfo = ClientThread(item)
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
                        threadInfo = WebSkClientThread(item)

                elif (skTy == 'BLUETOOTH'):
                    if (skConTy == 'SERVER'):
                        threadInfo = BlueToothServerThread(item)
                    elif (skConTy == 'CLIENT'):
                        threadInfo = BlueToothClientThread(item)

                elif (skTy == 'PLC'):
                    if (skConTy == 'SERVER'):
                        threadInfo = ServerUdpThread(item)
                    elif (skConTy == 'CLIENT'):
                        threadInfo = ClientUdpThread(item)

                elif (skTy == 'HTTP(S)'):
                    if (skConTy == 'SERVER'):
                        threadInfo = HttpServerThread(item)

                else:
                    logger.info(f'None condition')
                    continue

                item['SK_THREAD'] = threadInfo
                self.handlPop.ui.combo_sk_list.addItem(item['SK_ID'])
                self.ui.main_combo_sk_list.addItem(item['SK_ID'])
                self.directPop.ui.dir_sk.addItem(item['SK_ID'])

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
            logger.error(f'Init.start_sk() Exception :: {traceback.format_exc()}')



    def setGrid(self):
        self.ui.list_run_server.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.list_run_server.verticalHeader().setVisible(False)  # 행 번호 헤더 숨기기
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


        # --- 테이블 설정 ---
        self.ui.list_run_plc.setRowCount(0)
        self.ui.list_run_plc.setColumnCount(4)
        self.ui.list_run_plc.setHorizontalHeaderLabels(
            ["PLC_ID", "UPD_DT", "ADDR", "DATA"]
        )

        # 행 번호 헤더 숨기기
        self.ui.list_run_plc.verticalHeader().setVisible(False)

        # 컬럼 헤더
        header = self.ui.list_run_plc.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Fixed)   # 모든 칼럼을 고정모드로

        # 각 칼럼 너비 지정
        self.ui.list_run_plc.setColumnWidth(0, 100)   # PLC_ID
        self.ui.list_run_plc.setColumnWidth(1, 80)   # UPD_DT
        self.ui.list_run_plc.setColumnWidth(2, 80)   # ADDR

        header.setSectionResizeMode(0, QHeaderView.Fixed)
        header.setSectionResizeMode(1, QHeaderView.Fixed)
        header.setSectionResizeMode(2, QHeaderView.Fixed)
        header.setSectionResizeMode(3, QHeaderView.Stretch)



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

    def open_plc_settings(self):
        if self.plc_popup.isVisible():
            # self.popup.instance.hide()
            self.plc_popup.hide()
        else:
            # self.popup.instance.show()
            self.plc_popup.show()

    def open_util(self):
        if self.utilityPop.isVisible():
            # self.popup.instance.hide()
            self.utilityPop.hide()
        else:
            # self.popup.instance.show()
            self.utilityPop.show()

    def open_direct(self):
        if self.directPop.isVisible():
            self.directPop.hide()
        else:
            self.directPop.show()

    def open_settings(self):
        if self.popup.isVisible():
            self.popup.hide()
        else:
            self.popup.show()

    def open_handler(self):
        # if self.handlPop.isVisible():
        #     self.handlPop.hide()
        # else:
        #     self.handlPop.show()

        if self.sqlHandler.isVisible():
            self.sqlHandler.hide()
        else:
            self.sqlHandler.show()


    def open_logger(self):
        # 열고 싶은 경로
        # path = r"../logs/"
        # current_path = os.getcwd()
        # logger.info(f'path : {current_path}')
        # # 경로 열기
        # os.startfile(f'{current_path}/logs')
        if self.logPop.isVisible():
            self.logPop.hide()
        else:
            self.logPop.show()


    def closeMain(self):
        logger.info(f'close ``````````````````````````')

    @Slot()
    def workUpdateConnList(self):

        try:
            self.treeModel.clear()  # 모델의 모든 항목 제거
            # self.treeModel.setHorizontalHeaderLabels(["SK_ID", "Description"])  # 헤더 다시 설정
            self.treeModel.setHorizontalHeaderLabels(["connection Info"])  # 헤더 다시 설정
            self.root_node = self.treeModel.invisibleRootItem()
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

    @Slot(str)
    def insertLog(self,msg):
        try:
            if "recive_string" in msg:
                self.ui.log_text_log.append(f'<span style="color:blue">{msg} <span/>')
            elif "send_string" in msg:
                self.ui.log_text_log.append(f'<span style="color:green">{msg} <span/>')
            else:
                self.ui.log_text_log.append(f'<span>{msg} <span/>')
        except:
            logger.error(f'showLog error : {traceback.format_exc()}')


    def clickClear(self):
        self.ui.log_text_log.clear()

    def openFolder(self):
        try:
            # 열고 싶은 경로
            path = r"../logs/"
            current_path = os.getcwd()
            # logger.info(f'path : {current_path}')
            # 경로 열기
            os.startfile(f'{current_path}/logs')
        except:
            traceback.format_exc()
