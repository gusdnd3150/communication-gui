from PySide6.QtGui import QBrush, QColor
from PySide6.QtWidgets import QTableWidgetItem, QMainWindow, QHeaderView, QMessageBox

from conf.skModule import *
from conf.sql.SystemQueryString import *
from ui.ui_plc_settings import Ui_PLC_Settings
from src.component.plcSettings.TapPlc import TapPlc
from src.component.plcSettings.TapAddr import TapAddr


class PlcSettings(QMainWindow):
    initData = None
    skRow = None
    contFlag = 'upd'
    contInFlag = 'upd'
    contBzFlag = 'upd'
    contSchFlag = 'upd'
    curMsg = ''
    gridData = []

    def __init__(self, initData):
        super(PlcSettings, self).__init__()
        self.initData = initData
        self.ui = Ui_PLC_Settings()
        self.ui.setupUi(self)
        self.setWindowTitle('PLC')

        self.setEvent()
        self.createGrid()
        # TapPlc(initData, self.ui) 이벤트 전파가 하위레벨에서는 안되는 것으로 보임
        # TapAddr(initData, self.ui)

    def setEvent(self):

        self.ui.list_plc.cellClicked.connect(self.selectRow)
        self.ui.btn_addPlc.clicked.connect(self.addPlc)
        self.ui.btn_savePlc.clicked.connect(self.savePlc)
        self.ui.btn_delPlc.clicked.connect(self.delPlc)
        self.ui.plc_search_plc.textChanged.connect(self.searchPlc)
        self.ui.plc_search_pkg.textChanged.connect(self.searchPlc)

        for item in useYnCombo:
            self.ui.PLC_USE_YN.addItem(item)
            self.ui.PLC_LOG_YN.addItem(item)

        for item in plcMakerCombo:
            self.ui.PLC_PLC_MAKER.addItem(item)

        for item in commTyCombo:
            self.ui.PLC_COMM_TY.addItem(item)

        for item in slotCombo:
            self.ui.PLC_SLOT.addItem(item)

        for item in rackCombo:
            self.ui.PLC_RACK.addItem(item)

        self.ui.PLC_PLC_MAKER.currentTextChanged.connect(self.onChangeMaker)

    def onChangeMaker(self, text):
        self.ui.PLC_CPU_TY.clear()
        self.ui.PLC_PROTOCOL.clear()

        if text == 'Simens':
            for item in simenCpuTyCombo:
                self.ui.PLC_CPU_TY.addItem(item)

            for item in simenProtocolCombo:
                self.ui.PLC_PROTOCOL.addItem(item)

        elif text == 'Mitsubishi':
            for item in mitsuCpuTyCombo:
                self.ui.PLC_CPU_TY.addItem(item)

            for item in mitsuProtocolCombo:
                self.ui.PLC_PROTOCOL.addItem(item)

    def selectRow(self, row, column):
        try:
            self.contFlag = 'upd'
            col_count = self.ui.list_plc.columnCount()
            row_data = {}
            for col in range(col_count):
                header_item = self.ui.list_plc.horizontalHeaderItem(col)
                header = header_item.text() if header_item else f"col{col}"

                item = self.ui.list_plc.item(row, col)
                value = item.text() if item else ""
                row_data[header] = value

            self.ui.PLC_PKG_ID.setText(row_data['PKG_ID'])
            self.ui.PLC_PKG_ID.setDisabled(True)
            self.ui.PLC_PLC_ID.setText(row_data['PLC_ID'])
            self.ui.PLC_PLC_ID.setDisabled(True)
            self.ui.PLC_PLC_IP.setText(row_data['PLC_IP'])
            self.ui.PLC_PLC_PORT.setText(row_data['PLC_PORT'])
            self.ui.PLC_USE_YN.setCurrentText(row_data['USE_YN'])
            self.ui.PLC_PLC_MAKER.setCurrentText(row_data['PLC_MAKER'])
            self.ui.PLC_CPU_TY.setCurrentText(row_data['CPU_TY'])
            self.ui.PLC_SLOT.setCurrentText(row_data['SLOT'])

            self.ui.PLC_RACK.setCurrentText(row_data['RACK'])
            self.ui.PLC_COMM_TY.setCurrentText(row_data['COMM_TY'])
            self.ui.PLC_LOG_YN.setCurrentText(row_data['LOG_YN'])
        except:
            logger.error(f'select row error {traceback.format_exc()}')

    def createGrid(self):
        try:
            headers = ['PKG_ID', 'PLC_ID', 'USE_YN', 'PLC_MAKER', 'PLC_PTOROTOCOL', 'CPU_TY', 'SLOT', 'RACK', 'PLC_IP',
                       'PLC_PORT', 'SK_LOG', 'COMM_TY', 'LOG_YN']

            self.ui.list_plc.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            self.ui.list_plc.verticalHeader().setVisible(False)
            self.ui.list_plc.setSortingEnabled(False)
            self.ui.list_plc.setRowCount(0)  # Table의 행을 설정, list의 길이
            self.ui.list_plc.setColumnCount(13)
            self.ui.list_plc.setHorizontalHeaderLabels(headers)
            pkg = self.ui.plc_search_pkg.text()
            plcId = self.ui.plc_search_plc.text()
            self.gridData = selectQuery(selectPlcList(plcId, None, pkg))
            for i, skItem in enumerate(self.gridData):
                row_count = self.ui.list_plc.rowCount()
                self.ui.list_plc.insertRow(row_count)
                for j, hd in enumerate(headers):
                    if skItem.get(hd) is not None:
                        self.ui.list_plc.setItem(row_count, j, QTableWidgetItem(str(skItem[hd])))

            # self.ui.list_plc.cellClicked.connect(self.selectRow)
            # self.ui.list_plc.currentCellChanged.connect(self.selectRow)
        except Exception as e:
            logger.info(f'createGrid exception : {traceback.format_exc()}')

    def addPlc(self):
        self.contFlag = 'ins'
        self.ui.PLC_PKG_ID.setText('')
        self.ui.PLC_PKG_ID.setDisabled(False)
        self.ui.PLC_PLC_ID.setText('')
        self.ui.PLC_PLC_ID.setDisabled(False)
        self.ui.PLC_PLC_IP.setText('')
        self.ui.PLC_PLC_PORT.setText('')
        self.ui.PLC_USE_YN.setCurrentText('')
        self.ui.PLC_PLC_MAKER.setCurrentText('')
        self.ui.PLC_CPU_TY.setCurrentText('')
        self.ui.PLC_SLOT.setCurrentText('')
        self.ui.PLC_RACK.setCurrentText('')
        self.ui.PLC_COMM_TY.setCurrentText('')
        self.ui.PLC_LOG_YN.setCurrentText('')

    def savePlc(self):

        pkgId = self.ui.PLC_PKG_ID.text()
        plcId = self.ui.PLC_PLC_ID.text()
        useYn = self.ui.PLC_USE_YN.currentText()
        maker = self.ui.PLC_PLC_MAKER.currentText()
        protocol = self.ui.PLC_PROTOCOL.currentText()
        cpuTy = self.ui.PLC_CPU_TY.currentText()
        slot = self.ui.PLC_SLOT.currentText()
        rack = self.ui.PLC_RACK.currentText()
        commTy = self.ui.PLC_COMM_TY.currentText()
        plcIp = self.ui.PLC_PLC_IP.text()
        plcPort = self.ui.PLC_PLC_PORT.text()
        logYn = self.ui.PLC_LOG_YN.currentText()

        # plcId = self.ui.
        row_data = {
            'PLC_ID': plcId,
            'PKG_ID': pkgId,
            'USE_YN': useYn,
            'PLC_MAKER': maker,
            'PLC_PTOROTOCOL': protocol,
            'CPU_TY': cpuTy,
            'SLOT': slot,
            'RACK': rack,
            'COMM_TY': commTy,
            'PLC_IP': plcIp,
            'PLC_PORT': plcPort,
            'LOG_YN': logYn
        }
        if self.contFlag == 'ins':
            queryExecute(insertTable(row_data, 'TB_SK_PKG_PLC'))
        else:
            queryExecute(saveTable('TB_SK_PKG_PLC', ['PKG_ID', 'PLC_ID'], row_data))
        self.createGrid()

    def delPlc(self):
        pkgId = self.ui.PLC_PKG_ID.text()
        plcId = self.ui.PLC_PLC_ID.text()

        if pkgId != '' or plcId != '':
            row_data = {
                'PLC_ID': plcId,
                'PKG_ID': pkgId}
            queryExecute(deleteTable('TB_SK_PKG_PLC',['PKG_ID','PLC_ID'],row_data))
            self.createGrid()

    def searchPlc(self):
        try:
            self.createGrid()
        except Exception as e:
            logger.error(f'searchMsg exception : {traceback.format_exc()}')