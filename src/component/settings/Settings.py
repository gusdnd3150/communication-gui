from PySide6.QtGui import QBrush, QColor
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QTableWidgetItem, QMainWindow, QHeaderView , QCheckBox, QWidget, QHBoxLayout, QMessageBox
import sys
import os
import traceback
from conf.skModule import *
from conf.sql.SystemQueryString import *
from ui.ui_settings import Ui_Settings

class Settings(QMainWindow):

    instance = None
    saveSkWindow = None
    initData = None
    skRow = None
    contFlag = 'upd'
    contInFlag = 'upd'
    contBzFlag = 'upd'
    contSchFlag = 'upd'
    addMsgList = [] # 추가할 row index를 저장
    addMsgDtList = []  # 추가할 row index를 저장
    curMsg = ''

    def __init__(self, initData):
        super(Settings, self).__init__()
        self.initData = initData
        self.ui = Ui_Settings()
        self.ui.setupUi(self)
        self.setWindowTitle('설정')
        self.setEvent()
        self.createSkGrid() # 소켓 그리드
        self.createInGrid()# 소켓 In 그리드
        self.createBzGrid()
        self.createSchGrid()
        self.createMsgGrid(None,None)# 메시지 그리드


    def setEvent(self):

        # 소켓 탭 이벤트 설정
        self.ui.btn_addSk.clicked.connect(self.addSk)
        self.ui.btn_delSk.clicked.connect(self.delSk)
        self.ui.btn_saveSk.clicked.connect(self.saveSk)

        # In 탭 이벤트 설정
        self.ui.btn_addIn.clicked.connect(self.addIn)
        self.ui.btn_delIn.clicked.connect(self.delIn)
        self.ui.btn_saveIn.clicked.connect(self.saveIn)

        # 메시지 탭 이벤트 설정
        self.ui.msg_search.clicked.connect(self.searchMsg)

        self.ui.msg_add.clicked.connect(self.msgAddRow)
        self.ui.msg_save.clicked.connect(self.saveMsg)
        self.ui.msg_del.clicked.connect(self.delMsg)

        self.ui.msg_dt_add.clicked.connect(self.msgDtAddRow)
        self.ui.msg_dt_save.clicked.connect(self.saveMsgDt)
        self.ui.msg_dt_del.clicked.connect(self.delMsgDt)


        # 이벤트/ 스케줄 탭 이벤트 설정
        self.ui.btn_addBz.clicked.connect(self.addBz)
        self.ui.btn_delBz.clicked.connect(self.delBz)
        self.ui.btn_saveBz.clicked.connect(self.saveBz)

        self.ui.btn_addSch.clicked.connect(self.addSch)
        self.ui.btn_delSch.clicked.connect(self.delSch)
        self.ui.btn_saveSch.clicked.connect(self.saveSch)




        for item in useYnCombo:
            self.ui.sk_USE_YN.addItem(item)
            self.ui.sk_SK_LOG.addItem(item)
            self.ui.in_USE_YN.addItem(item)
            self.ui.bz_USE_YN.addItem(item)
            self.ui.sch_USE_YN.addItem(item)

        for item in skTypeCombo:
            self.ui.sk_SK_TYPE.addItem(item)

        for item in skConnCombo:
            self.ui.sk_SK_CONN_TYPE.addItem(item)

        for item in skClientCombo:
            self.ui.sk_SK_CLIENT_TYPE.addItem(item)
        for item in hdCombo:
            self.ui.sk_HD_ID.addItem(item)

        for item in jobTypeCombo:
            self.ui.sch_SCH_JOB_TYPE.addItem(item)

        for item in eventTypeCombo:
            self.ui.bz_BZ_TYPE.addItem(item)

    def createSkGrid(self):
        try:
            headers = ['PKG_ID', 'SK_ID','USE_YN', 'SK_GROUP', 'SK_TYPE', 'SK_CONN_TYPE', 'SK_CLIENT_TYPE', 'HD_ID', 'SK_IP',
                       'SK_PORT', 'SK_DELIMIT_TYPE', 'SK_LOG', 'SK_DESC']

            self.ui.list_sk.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            self.ui.list_sk.verticalHeader().setVisible(False)

            self.ui.list_sk.setRowCount(0)  # Table의 행을 설정, list의 길이
            self.ui.list_sk.setColumnCount(13)
            self.ui.list_sk.setHorizontalHeaderLabels(headers)
            skList = selectQuery(selectSocketList(None, None, None))
            for i, skItem in enumerate(skList):
                row_count = self.ui.list_sk.rowCount()
                self.ui.list_sk.insertRow(row_count)
                for j, hd in enumerate(headers):
                    if skItem.get(hd) is not None:
                        self.ui.list_sk.setItem(row_count, j, QTableWidgetItem(str(skItem[hd])))
            self.ui.list_sk.cellClicked.connect(self.selectRow)
            self.ui.list_sk.currentCellChanged.connect(self.selectRow)

        except Exception as e:
            logger.info(f'createGrid exception : {traceback.format_exc()}')


    def selectRow(self,row, column):
        try:
            self.contFlag = 'upd'
            # logger.info(f'row: {row}')
            # item = self.ui.list_sk.item(row, column)
            # if item:
            #     print(f"Item text: {item.text()}")
            row_data = {}
            for column in range(self.ui.list_sk.columnCount()):
                header_item = self.ui.list_sk.horizontalHeaderItem(column)
                item = self.ui.list_sk.item(row, column)
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
        if self.contFlag == 'ins':
            row_data['SK_ID'] = self.ui.sk_SK_ID.text()
            row_data['PKG_ID'] = self.ui.sk_PKG_ID.text()
            queryExecute(insertSK(row_data))
        else :
            queryExecute(saveSk(self.ui.sk_PKG_ID.text(), self.ui.sk_SK_ID.text(), row_data))
        self.createSkGrid()
        logger.info(f'{row_data}')

#################################################################### 소켓 IN
    def createInGrid(self):
        try:
            headers = ['PKG_ID','SK_IN_SEQ','IN_SK_ID','IN_MSG_ID','BZ_METHOD','IN_DESC','USE_YN']
            self.ui.list_in.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            self.ui.list_in.verticalHeader().setVisible(False)

            self.ui.list_in.setRowCount(0)  # Table의 행을 설정, list의 길이
            self.ui.list_in.setColumnCount(7)
            self.ui.list_in.setHorizontalHeaderLabels(headers)
            inList = selectQuery(selectSocketInList(None, None, None))
            for i, inItem in enumerate(inList):
                row_count = self.ui.list_in.rowCount()
                self.ui.list_in.insertRow(row_count)
                for j, hd in enumerate(headers):
                    if inItem.get(hd) is not None:
                        self.ui.list_in.setItem(row_count, j, QTableWidgetItem(str(inItem[hd])))
            self.ui.list_in.cellClicked.connect(self.selectInRow)
            self.ui.list_in.currentCellChanged.connect(self.selectInRow)
        except Exception as e:
            logger.info(f'createGrid exception : {traceback.format_exc()}')

    def addIn(self):
        self.contInFlag = 'ins'
        self.skRow = None
        self.ui.in_PKG_ID.setText('')
        self.ui.in_PKG_ID.setDisabled(False)
        self.ui.in_SK_IN_SEQ.setText('')
        self.ui.in_SK_IN_SEQ.setDisabled(False)

        self.ui.in_IN_SK_ID.setText('')
        self.ui.in_IN_SK_ID.setDisabled(False)

        self.ui.in_IN_MSG_ID.setText('')
        self.ui.in_BZ_METHOD.setText('')
        self.ui.in_IN_DESC.setText('')


    def delIn(self):
        queryExecute(delIn(self.ui.in_PKG_ID.text(), self.ui.in_SK_IN_SEQ.text()))
        self.createInGrid()

    def saveIn(self):
        row_data = {
            'IN_SK_ID': self.ui.in_IN_SK_ID.text()
            , 'IN_MSG_ID': self.ui.in_IN_MSG_ID.text()
            , 'BZ_METHOD': self.ui.in_BZ_METHOD.text()
            , 'USE_YN': self.ui.in_USE_YN.currentText()
            , 'IN_DESC': self.ui.in_IN_DESC.toPlainText()
        }
        logger.info(f' row : {row_data}')
        if self.contInFlag == 'ins':
            row_data['PKG_ID'] = self.ui.in_PKG_ID.text()
            row_data['SK_IN_SEQ'] = self.ui.in_SK_IN_SEQ.text()
            queryExecute(insertIn(row_data))
        else :
            queryExecute(saveIn(self.ui.in_PKG_ID.text(),self.ui.in_IN_SK_ID.text(), self.ui.in_SK_IN_SEQ.text(), row_data))
        self.createInGrid()

    def selectInRow(self,row, column):
        try:
            self.contInFlag = 'upd'
            # logger.info(f'row: {row}')
            # item = self.ui.list_sk.item(row, column)
            # if item:
            #     print(f"Item text: {item.text()}")
            row_data = {}
            for column in range(self.ui.list_in.columnCount()):
                header_item = self.ui.list_in.horizontalHeaderItem(column)
                item = self.ui.list_in.item(row, column)
                row_data[header_item.text()] = item.text() if item else ""
            self.skRow = row
            self.ui.in_PKG_ID.setText(row_data['PKG_ID'])
            self.ui.in_PKG_ID.setDisabled(True)
            self.ui.in_SK_IN_SEQ.setText(row_data['SK_IN_SEQ'])
            self.ui.in_SK_IN_SEQ.setDisabled(True)

            self.ui.in_IN_SK_ID.setText(row_data['IN_SK_ID'])
            self.ui.in_IN_SK_ID.setDisabled(True)

            self.ui.in_IN_MSG_ID.setText(row_data['IN_MSG_ID'])
            self.ui.in_BZ_METHOD.setText(row_data['BZ_METHOD'])
            self.ui.in_IN_DESC.setText(row_data['IN_DESC'])
            self.ui.in_USE_YN.setCurrentText(row_data['USE_YN'])

        except Exception as e :
            logger.error(f'selectRow exception : {traceback.format_exc()} ')
#################################################################### 메시지

    def searchMsg(self):
        try:
            self.addMsgList.clear()
            self.createMsgGrid(self.ui.msg_MSG_ID_iq.text(),self.ui.msg_MSG_MID_iq.text())
            self.createMsgDtGrid(self.ui.msg_MSG_ID_iq.text())
        except Exception as e:
            logger.error(f'searchMsg exception : {traceback.format_exc()}')


    def createMsgGrid(self, msg, mid):
        try:
            headers = ['MSG_ID','MSG_KEY_TYPE','MSG_KEY_VAL','MSG_DESC' ]
            self.ui.msg_list.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            self.ui.msg_list.setRowCount(0)  # Table의 행을 설정, list의 길이
            self.ui.msg_list.setColumnCount(4)
            self.ui.msg_list.setHorizontalHeaderLabels(headers)
            skList = selectQuery(selectSocketMSgList(msg, mid))
            for i, skItem in enumerate(skList):
                row_count = self.ui.msg_list.rowCount()
                self.ui.msg_list.insertRow(row_count)
                for j, hd in enumerate(headers):

                    if skItem.get(hd) is not None:
                        self.ui.msg_list.setItem(row_count, j, QTableWidgetItem(str(skItem[hd])))
            self.ui.msg_list.cellClicked.connect(self.selectMsgRow)
            self.ui.msg_list.currentCellChanged.connect(self.selectMsgRow)
        except Exception as e:
            logger.error(f'createMsgGrid exception : {traceback.format_exc()}')

    def selectMsgRow(self,row, column):
        try:
            row_data = self.getMsgByRownum(row)
            self.ui.selected_msg.setText(row_data['MSG_ID'])
            self.createMsgDtGrid(row_data['MSG_ID'])
        except Exception as e :
            logger.error(f'selectMsgRow exception : {traceback.format_exc()} ')

    def createMsgDtGrid(self, msg):
        try:
            if msg is None or msg == '':
                return

            headers = ['MSG_DT_ORD','MSG_DT_VAL_ID','MSG_DT_DESC','VAL_TYPE','VAL_LEN' ]
            self.ui.msg_dt_list.setRowCount(0)  # Table의 행을 설정, list의 길이
            self.ui.msg_dt_list.setColumnCount(5)
            self.ui.msg_dt_list.verticalHeader().setVisible(False)  # 행 번호 헤더 숨기기
            self.ui.msg_dt_list.setHorizontalHeaderLabels(headers)
            skList = selectQuery(selectSocketMSgDtList(msg))
            for i, skItem in enumerate(skList):
                row_count = self.ui.msg_dt_list.rowCount()
                self.ui.msg_dt_list.insertRow(row_count)
                for j, hd in enumerate(headers):

                    if skItem.get(hd) is not None:
                        self.ui.msg_dt_list.setItem(row_count, j, QTableWidgetItem(str(skItem[hd])))
            # self.ui.msg_dt_list.cellClicked.connect(self.selectMsgRow)
        except Exception as e:
            logger.error(f'createMsgGrid exception : {traceback.format_exc()}')


    def msgAddRow(self):
        try:
            self.ui.msg_list.setRowCount(0)
            row_count = self.ui.msg_list.rowCount()
            self.ui.msg_list.insertRow(row_count)
            headers = ['MSG_ID', 'MSG_KEY_TYPE', 'MSG_KEY_VAL', 'MSG_DESC']
            for j, hd in enumerate(headers):
                item = QTableWidgetItem('')
                item.setBackground(QBrush(QColor(148, 127, 127)))  # 노란색 배경 설정
                item.setForeground(QBrush(QColor(0, 0, 0)))
                self.ui.msg_list.setItem(row_count, j, item)
                
            self.addMsgList.append(row_count)
        except:
            logger.error(f'test')

    def saveMsg(self):
        try:
            logger.info(f'saveMsg')
            upd_rows = []
            if len(self.addMsgList) > 0 :
                for index, rowNum in enumerate(self.addMsgList):
                    upd_rows.append(self.getMsgByRownum(rowNum))

                for ins, item in enumerate(upd_rows):
                    rslt = selectQueryAsInt(selectMsgBodyCnt(item['MSG_ID']))
                    if rslt < 1:
                        queryExecute(insertMsgBody(item))
                    else:
                        queryExecute(updateMsgBody(item))
            else:
                curIndex = self.ui.msg_list.currentRow()
                row_data = self.getMsgByRownum(curIndex)
                logger.info(f' 업데이트 테[스트 : {row_data}')
                queryExecute(updateMsgBody(row_data))
        except:
            logger.error(f'saveMsg error : {traceback.format_exc()}')
        finally:
            self.addMsgList.clear()
            self.searchMsg()

    def delMsg(self):
        try:
            msgId = self.ui.selected_msg.text()
            if msgId != '':

                queryExecute(deleteMsgBody(msgId))
                queryExecute(deleteMsgBodyDt(msgId))
        except:
            logger.error(f'saveMsg error : {traceback.format_exc()}')
        finally:
            self.curMsg = ''
            self.searchMsg()
            # self.addMsgList.clear()
            # self.searchMsg()

    def getMsgByRownum(self, rownum):
        row_data = {}
        try:
            for column in range(self.ui.msg_list.columnCount()):
                header_item = self.ui.msg_list.horizontalHeaderItem(column)
                item = self.ui.msg_list.item(rownum, column)
                row_data[header_item.text()] = item.text() if item else ""
        except:
            logger.error(f'getMsgByRownum exceptoon : {traceback.format_exc()}')
        return row_data


    def getMsgDtByRownum(self, rownum):
        row_data = {}
        try:
            for column in range(self.ui.msg_dt_list.columnCount()):
                header_item = self.ui.msg_dt_list.horizontalHeaderItem(column)
                item = self.ui.msg_dt_list.item(rownum, column)
                row_data[header_item.text()] = item.text() if item else ""
        except:
            logger.error(f'getMsgDtByRownum exceptoon : {traceback.format_exc()}')
        return row_data

    def msgDtAddRow(self):
        try:
            targetMsg = self.ui.selected_msg.text()
            if targetMsg is not None and targetMsg != '':
                # self.ui.msg_dt_list.setRowCount(0)
                row_count = self.ui.msg_dt_list.rowCount()
                self.ui.msg_dt_list.insertRow(row_count)
                headers = ['MSG_DT_ORD','MSG_DT_VAL_ID','MSG_DT_DESC','VAL_TYPE','VAL_LEN' ]
                for j, hd in enumerate(headers):
                    item = QTableWidgetItem('')
                    item.setBackground(QBrush(QColor(148, 127, 127)))  # 노란색 배경 설정
                    item.setForeground(QBrush(QColor(0, 0, 0)))
                    self.ui.msg_dt_list.setItem(row_count, j, item)

                # self.addMsgDtList.append(row_count)
        except:
            logger.error(f'msgDtAddRow exception :: {traceback.format_exc()}')

    def saveMsgDt(self):
        try:
            targetMsg = self.ui.selected_msg.text()

            if(self.checkPop(targetMsg,f' {targetMsg} 데이터를 저장하시겠습니까')):
                upd_rows = []
                row_count = self.ui.msg_dt_list.rowCount()
                for index in range(row_count):
                    obj = self.getMsgDtByRownum(index)
                    obj['MSG_ID'] = targetMsg
                    upd_rows.append(obj)

                logger.info(f'ddddddd :: {upd_rows}')
                queryExecute(f'DELETE FROM TB_SK_MSG_BODY_DT WHERE MSG_ID ="{targetMsg}"')
                for ix, item in enumerate(upd_rows):
                    # DT 테이블에 새롭게 INSERT
                    insertRow = {
                        'MSG_ID':item['MSG_ID']
                        ,'MSG_DT_ORD':item['MSG_DT_ORD']
                        ,'MSG_DT_VAL_ID':item['MSG_DT_VAL_ID']
                    }
                    queryExecute(insertMsgBodyDt(insertRow))
                    cnt = selectQueryAsInt(F'SELECT COUNT(1) FROM TB_SK_MSG_VAL WHERE VAL_ID = "{item["MSG_DT_VAL_ID"]}"')
                    if cnt < 1:
                        insertRow2 = {
                            'VAL_ID': item['MSG_DT_VAL_ID']
                            , 'VAL_TYPE': item['VAL_TYPE']
                            , 'VAL_LEN': item['VAL_LEN']
                        }
                        queryExecute(insertMsgVal(insertRow2))
                self.createMsgDtGrid(targetMsg)

        except:
            logger.error(f'saveMsgDt error : {traceback.format_exc()}')
        finally:

            logger.info(f'saveMsgDt done')
            # self.addMsgDtList.clear()

    def delMsgDt(self):
        try:
            targetMsg = self.ui.selected_msg.text()
            row_count = self.ui.msg_dt_list.currentRow()
            obj = self.getMsgDtByRownum(row_count)
            targetVal  = obj['MSG_DT_VAL_ID']
            if self.checkPop(f'{targetMsg}', f'{obj} - {targetVal}를 삭제 하시겠습니까?'):
                queryExecute(F'DELETE FROM TB_SK_MSG_BODY_DT WHERE MSG_ID = "{targetMsg}" AND MSG_DT_VAL_ID = "{targetVal}"')
                self.createMsgDtGrid(targetMsg)
        except:
            logger.error(f'delMsgDt exception ::{traceback.format_exc()}')

#################################################################### 이벤트 설정
    def createBzGrid(self):
        try:
            headers = ['PKG_ID','SK_GROUP','BZ_TYPE','USE_YN','BZ_METHOD','SEC','BZ_DESC']
            self.ui.list_bz.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            self.ui.list_bz.verticalHeader().setVisible(False)

            self.ui.list_bz.setRowCount(0)  # Table의 행을 설정, list의 길이
            self.ui.list_bz.setColumnCount(7)
            self.ui.list_bz.setHorizontalHeaderLabels(headers)
            # inList = selectQuery(selectSocketInList(None, None, None))
            inList = selectQuery(selectBzList(None, None, None))
            for i, inItem in enumerate(inList):
                row_count = self.ui.list_bz.rowCount()
                self.ui.list_bz.insertRow(row_count)
                for j, hd in enumerate(headers):
                    if inItem.get(hd) is not None:
                        self.ui.list_bz.setItem(row_count, j, QTableWidgetItem(str(inItem[hd])))
            self.ui.list_bz.cellClicked.connect(self.selectBzRow)
            self.ui.list_bz.currentCellChanged.connect(self.selectBzRow)
        except Exception as e:
            logger.info(f'createBzGrid exception : {traceback.format_exc()}')

    def addBz(self):
        self.contBzFlag = 'ins'
        self.skRow = None
        self.ui.bz_PKG_ID.setText('')
        self.ui.bz_SK_GROUP.setText('')
        self.ui.bz_BZ_METHOD.setText('')
        self.ui.bz_SEC.setText('')
        self.ui.bz_BZ_DESC.setText('')

        self.ui.bz_PKG_ID.setDisabled(False)
        self.ui.bz_SK_GROUP.setDisabled(False)
        self.ui.bz_BZ_TYPE.setDisabled(False)


    def delBz(self):
        queryExecute(delBz(self.ui.bz_PKG_ID.text(), self.ui.bz_SK_GROUP.text(), self.ui.bz_BZ_TYPE.currentText()))
        self.createBzGrid()

    def saveBz(self):
        row_data = {
            'PKG_ID':self.ui.bz_PKG_ID.text()
            , 'SK_GROUP': self.ui.bz_SK_GROUP.text()
            , 'BZ_TYPE': self.ui.bz_BZ_TYPE.currentText()
            , 'USE_YN': self.ui.bz_USE_YN.currentText()
            , 'BZ_METHOD': self.ui.bz_BZ_METHOD.text()
            , 'SEC': self.ui.bz_SEC.text()
            , 'BZ_DESC': self.ui.bz_BZ_DESC.toPlainText()
        }
        logger.info(f' row : {row_data}')
        if self.contBzFlag == 'ins':
            queryExecute(insertTable(row_data,'TB_SK_PKG_SK_BZ'))
        else :
            queryExecute(saveBz(self.ui.bz_PKG_ID.text(), self.ui.bz_SK_GROUP.text(),self.ui.bz_BZ_TYPE.currentText(), row_data))
        self.createBzGrid()

    def selectBzRow(self,row, column):
        try:
            self.contBzFlag = 'upd'
            row_data = {}
            for column in range(self.ui.list_bz.columnCount()):
                header_item = self.ui.list_bz.horizontalHeaderItem(column)
                item = self.ui.list_bz.item(row, column)
                row_data[header_item.text()] = item.text() if item else ""
            self.skRow = row
            self.ui.bz_PKG_ID.setText(row_data['PKG_ID'])
            self.ui.bz_PKG_ID.setDisabled(True)
            self.ui.bz_SK_GROUP.setText(row_data['SK_GROUP'])
            self.ui.bz_SK_GROUP.setDisabled(True)
            self.ui.bz_BZ_METHOD.setText(row_data['BZ_METHOD'])

            self.ui.bz_SEC.setText(row_data['SEC'])
            self.ui.bz_BZ_DESC.setText(row_data['BZ_DESC'])
            self.ui.bz_USE_YN.setCurrentText(row_data['USE_YN'])
            self.ui.bz_BZ_TYPE.setCurrentText(row_data['BZ_TYPE'])
            self.ui.bz_BZ_TYPE.setDisabled(True)

        except Exception as e :
            logger.error(f'selectBzRow exception : {traceback.format_exc()} ')
            



#################################################################### 스케줄 설정
    def createSchGrid(self):
        try:
            headers = ['PKG_ID','SCH_ID','SCH_JOB_TYPE','SCH_JOB','BZ_METHOD','SCH_DESC','USE_YN']

            # self.ui.list_in.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            self.ui.list_sch.verticalHeader().setVisible(False)

            self.ui.list_sch.setRowCount(0)  # Table의 행을 설정, list의 길이
            self.ui.list_sch.setColumnCount(7)
            self.ui.list_sch.setHorizontalHeaderLabels(headers)
            # inList = selectQuery(selectSocketInList(None, None, None))
            inList = selectQuery(selectSchList( None, None))
            for i, inItem in enumerate(inList):
                row_count = self.ui.list_sch.rowCount()
                self.ui.list_sch.insertRow(row_count)
                for j, hd in enumerate(headers):
                    if inItem.get(hd) is not None:
                        self.ui.list_sch.setItem(row_count, j, QTableWidgetItem(str(inItem[hd])))
            self.ui.list_sch.cellClicked.connect(self.selectSchRow)
            self.ui.list_sch.currentCellChanged.connect(self.selectSchRow)
        except Exception as e:
            logger.info(f'createSchGrid exception : {traceback.format_exc()}')

    def addSch(self):
        self.contSchFlag = 'ins'
        self.ui.sch_PKG_ID.setText('')
        self.ui.sch_PKG_ID.setDisabled(False)
        self.ui.sch_SCH_ID.setText('')
        self.ui.sch_SCH_ID.setDisabled(False)
        self.ui.sch_SCH_JOB.setText('')
        self.ui.sch_SCH_DESC.setText('')
        self.ui.sch_BZ_METHOD.setText('')

    def delSch(self):
        queryExecute(delSch(self.ui.sch_PKG_ID.text(), self.ui.sch_SCH_ID.text()))
        self.createSchGrid()

    def saveSch(self):
        row_data = {
            'PKG_ID':self.ui.sch_PKG_ID.text()
            , 'SCH_ID': self.ui.sch_SCH_ID.text()
            , 'SCH_JOB_TYPE': self.ui.sch_SCH_JOB_TYPE.currentText()
            , 'SCH_JOB': self.ui.sch_SCH_JOB.text()
            , 'BZ_METHOD': self.ui.sch_BZ_METHOD.text()
            , 'USE_YN': self.ui.sch_USE_YN.currentText()
            , 'SCH_DESC': self.ui.sch_SCH_DESC.toPlainText()
        }
        logger.info(f' row : {row_data}')
        if self.contSchFlag == 'ins':
            queryExecute(insertTable(row_data,'TB_SK_PKG_SCH'))
        else :
            queryExecute(saveSch(self.ui.sch_PKG_ID.text(), self.ui.sch_SCH_ID.text(),row_data))
        self.createSchGrid()

    def selectSchRow(self,row, column):
        try:
            self.contSchFlag = 'upd'
            row_data = {}
            for column in range(self.ui.list_sch.columnCount()):
                header_item = self.ui.list_sch.horizontalHeaderItem(column)
                item = self.ui.list_sch.item(row, column)
                row_data[header_item.text()] = item.text() if item else ""

            # self.ui.bz_PKG_ID.setDisabled(True)
            self.ui.sch_PKG_ID.setText(row_data['PKG_ID'])
            self.ui.sch_PKG_ID.setDisabled(True)
            self.ui.sch_SCH_ID.setText(row_data['SCH_ID'])
            self.ui.sch_SCH_ID.setDisabled(True)
            self.ui.sch_SCH_JOB.setText(row_data['SCH_JOB'])
            self.ui.sch_SCH_DESC.setText(row_data['SCH_DESC'])
            self.ui.sch_BZ_METHOD.setText(row_data['BZ_METHOD'])
            self.ui.sch_USE_YN.setCurrentText(row_data['USE_YN'])
            self.ui.sch_SCH_JOB_TYPE.setCurrentText(row_data['SCH_JOB_TYPE'])

        except Exception as e :
            logger.error(f'selectSchRow exception : {traceback.format_exc()} ')


    def checkPop(self, title ,msg):
        reply = QMessageBox.question(self,title, msg,QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            return True
        else:
            return False

