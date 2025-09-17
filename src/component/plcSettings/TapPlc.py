from PySide6.QtGui import QBrush, QColor
from PySide6.QtWidgets import QTableWidgetItem, QMainWindow, QHeaderView ,QMessageBox
from conf.skModule import *
from conf.sql.SystemQueryString import *

class TapPlc():

    ui = None
    initData = None
    gridData =[]

    def __init__(self, initData, ui):
        self.ui=ui
        self.initData=initData
        self.setEvent()
        self.createGrid()

    def setEvent(self):
        print()
        # 소켓 탭 이벤트 설정

        # self.ui.btn_delSk.clicked.connect(self.delSk)
        # self.ui.btn_saveSk.clicked.connect(self.saveSk)
        # self.ui.sk_search_pkg.textChanged.connect(self.searchSk)
        # self.ui.sk_search_sk.textChanged.connect(self.searchSk)


    def createGrid(self):
        try:
            headers = ['PKG_ID', 'SK_ID','USE_YN', 'SK_GROUP', 'SK_TYPE', 'SK_CONN_TYPE', 'SK_CLIENT_TYPE', 'HD_ID', 'SK_IP',
                       'SK_PORT', 'SK_DELIMIT_TYPE', 'SK_LOG', 'SK_DESC']

            self.ui.list_plc.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            self.ui.list_plc.verticalHeader().setVisible(False)
            self.ui.list_plc.setSortingEnabled(False)
            self.ui.list_plc.setRowCount(0)  # Table의 행을 설정, list의 길이
            self.ui.list_plc.setColumnCount(13)
            self.ui.list_plc.setHorizontalHeaderLabels(headers)
            # pkg = self.ui.sk_search_pkg.text()
            # skId = self.ui.sk_search_sk.text()
            # self.skList = selectQuery(selectSocketList(skId, None, pkg))
            # for i, skItem in enumerate(self.skList):
            #     row_count = self.ui.list_plc.rowCount()
            #     self.ui.list_plc.insertRow(row_count)
            #     for j, hd in enumerate(headers):
            #         if skItem.get(hd) is not None:
            #             self.ui.list_plc.setItem(row_count, j, QTableWidgetItem(str(skItem[hd])))
            # self.ui.list_plc.cellClicked.connect(self.selectRow)
            # self.ui.list_plc.currentCellChanged.connect(self.selectRow)
            # self.ui.list_plc.itemChanged.connect(self.onChangSkTable)

        except Exception as e:
            logger.info(f'createGrid exception : {traceback.format_exc()}')


    def onChangSkTable(self,item):
        try:
            row = item.row()
            column = item.column()
            value = item.text()

            key = self.ui.list_plc.horizontalHeaderItem(column).text()
            value = self.ui.list_plc.item(row, column).text()
            actualRow = self.skList[row]
            actualVal = str(actualRow[key])
            if actualVal == value:
                return

            # logger.info(f'key :{key} ,val {value},  actualRow:{actualRow}')

            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Information)  # 아이콘 유형: 정보
            msg_box.setWindowTitle("Alert")  # 팝업 창 제목
            # msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)  # 버튼 추가
            if key == 'PKG_ID' or key == 'SK_ID':
                self.ui.list_plc.setItem(row, column, QTableWidgetItem(str(actualRow[key])))
                msg_box.setText(f"{key}는 수정할 수 없습니다.")  # 팝업 메시지
                result = msg_box.exec()
            else:
                logger.info(f' row update')
                newObj = {
                    key:value
                }
                queryExecute(saveSk(actualRow['PKG_ID'], actualRow['SK_ID'], newObj))

                msg_box.setText(f"{key} update completed")  # 팝업 메시지
                result = msg_box.exec()


        except:
            logger.error(f'onChangInSkTable exception :: {traceback.format_exc()}')



    def selectRow(self,row, column):
        try:
            self.contFlag = 'upd'
            # logger.info(f'row: {row}')
            # item = self.ui.list_plc.item(row, column)
            # if item:
            #     print(f"Item text: {item.text()}")
            row_data = {}
            for column in range(self.ui.list_plc.columnCount()):
                header_item = self.ui.list_plc.horizontalHeaderItem(column)
                item = self.ui.list_plc.item(row, column)
                row_data[header_item.text()] = item.text() if item else ""
            self.skRow = row
            self.ui.sk_PKG_ID.setText(row_data['PKG_ID'])
            self.ui.sk_PKG_ID.setDisabled(True)
            self.ui.sk_SK_ID.setText(row_data['SK_ID'])
            self.ui.sk_SK_ID.setDisabled(True)
            self.ui.sk_SK_GROUP.setText(row_data['SK_GROUP'])
            self.ui.sk_SK_IP.setText(row_data['SK_IP'])
            self.ui.sk_SK_PORT.setText(row_data['SK_PORT'])
            self.ui.sk_SK_DELIMIT_TYPE.setText(row_data['SK_DELIMIT_TYPE'])
            self.ui.sk_SK_DESC.setText(row_data['SK_DESC'])
            self.ui.sk_SK_TYPE.setCurrentText(row_data['SK_TYPE'])
            self.ui.sk_USE_YN.setCurrentText(row_data['USE_YN'])
            self.ui.sk_SK_CONN_TYPE.setCurrentText(row_data['SK_CONN_TYPE'])
            self.ui.sk_SK_CLIENT_TYPE.setCurrentText(row_data['SK_CLIENT_TYPE'])
            self.ui.sk_HD_ID.setCurrentText(row_data['HD_ID'])
            self.ui.sk_SK_LOG.setCurrentText(row_data['SK_LOG'])


        except Exception as e :
            logger.error(f'selectRow exception : {traceback.format_exc()} ')

    def addSk(self):
        self.contFlag = 'ins'
        self.skRow = None
        self.ui.sk_PKG_ID.setText('')
        self.ui.sk_PKG_ID.setDisabled(False)
        self.ui.sk_SK_ID.setText('')
        self.ui.sk_SK_ID.setDisabled(False)
        self.ui.sk_SK_GROUP.setText('')
        self.ui.sk_SK_IP.setText('')
        self.ui.sk_SK_PORT.setText('')
        self.ui.sk_SK_DELIMIT_TYPE.setText('')
        self.ui.sk_SK_DESC.setText('')


    def delSk(self):
        logger.info(f'delete row : {self.skRow}')
        queryExecute(delSk(self.ui.sk_PKG_ID.text(), self.ui.sk_SK_ID.text()))
        self.createSkGrid()

    def saveSk(self):
        row_data = {
            'SK_GROUP': self.ui.sk_SK_GROUP.text()
            , 'USE_YN': self.ui.sk_USE_YN.currentText()
            , 'SK_TYPE': self.ui.sk_SK_TYPE.currentText()
            , 'SK_CONN_TYPE': self.ui.sk_SK_CONN_TYPE.currentText()
            , 'SK_CLIENT_TYPE': self.ui.sk_SK_CLIENT_TYPE.currentText()
            , 'HD_ID': self.ui.sk_HD_ID.currentText()
            , 'SK_IP': self.ui.sk_SK_IP.text()
            , 'SK_PORT': self.ui.sk_SK_PORT.text()
            , 'SK_LOG': self.ui.sk_SK_LOG.currentText()
            , 'SK_DELIMIT_TYPE': self.ui.sk_SK_DELIMIT_TYPE.text()
            , 'SK_DESC': self.ui.sk_SK_DESC.toPlainText()
        }

        if row_data['SK_TYPE'] == 'WEBSK' and row_data['SK_CONN_TYPE'] == 'SERVER':
            self.alertPop(f'{row_data['SK_TYPE']} {row_data["SK_CONN_TYPE"]}은 준비중입니다 . ')
            return


        if self.contFlag == 'ins':
            row_data['SK_ID'] = self.ui.sk_SK_ID.text()
            row_data['PKG_ID'] = self.ui.sk_PKG_ID.text()
            queryExecute(insertSK(row_data))
        else :
            queryExecute(saveSk(self.ui.sk_PKG_ID.text(), self.ui.sk_SK_ID.text(), row_data))
        self.createSkGrid()
        logger.info(f'{row_data}')

    def searchSk(self):
        try:
            self.createSkGrid()
        except Exception as e:
            logger.error(f'searchMsg exception : {traceback.format_exc()}')
