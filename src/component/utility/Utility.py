
from PySide6.QtWidgets import QTableWidgetItem, QMainWindow, QHeaderView
from PySide6.QtGui import QColor, QBrush
import sys
import os
import struct

program_path = sys.argv[0]
program_directory = os.path.dirname(program_path)
import traceback
from conf.skModule import *
from conf.sql.SystemQueryString import *
from ui.ui_utilty import Ui_MainWindow
import base64


class Utility(QMainWindow):

    initData = None
    combos = ['decimal','hex','base64','binary','ascii']

    def __init__(self, initData):
        super(Utility, self).__init__()
        self.initData = initData
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('유틸리티')
        self.setEvent()


    def convertTableData(self, data):
        try:
            result = data.split(" ")
            header = ['INDEX','BYTE']
            self.ui.util_encode_table.setRowCount(0)  # 초기화
            self.ui.util_encode_table.setColumnCount(2)
            self.ui.util_encode_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            self.ui.util_encode_table.verticalHeader().setVisible(False)
            self.ui.util_encode_table.setSortingEnabled(False)
            self.ui.util_encode_table.setHorizontalHeaderLabels(header)

            for i, skItem in enumerate(result):
                row_count = self.ui.util_encode_table.rowCount()
                self.ui.util_encode_table.insertRow(row_count)
                item = QTableWidgetItem(str(i))
                # item.setBackground(QColor("green"))
                item.setForeground(QColor("green"))
                self.ui.util_encode_table.setItem(row_count, 0, item)
                self.ui.util_encode_table.setItem(row_count, 1, QTableWidgetItem(str(skItem)))
        except:
            logger.info(f'convertTableData except : {traceback.format_exc()}')


    def setEvent(self):
        self.ui.btn_util_hex.clicked.connect(self.btnHex)
        self.ui.btn_util_decimal.clicked.connect(self.btnDecimal)
        self.ui.btn_util_binuary.clicked.connect(self.btnBinary)
        self.ui.btn_util_base64.clicked.connect(self.btnBase64)
        self.ui.btn_util_ascii.clicked.connect(self.btnAscii)
        self.ui.util_combo.addItems(self.combos)

        self.ui.btn_short_big.clicked.connect(self.shortB)
        self.ui.btn_short_little.clicked.connect(self.shortL)

        self.ui.btn_double_big.clicked.connect(self.doubleB)
        self.ui.btn_double_little.clicked.connect(self.doubleL)

        self.ui.btn_int_big.clicked.connect(self.intB)
        self.ui.btn_int_little.clicked.connect(self.intL)

        self.ui.btn_float_big.clicked.connect(self.floatB)
        self.ui.btn_float_little.clicked.connect(self.floatL)



    def btnHex(self):
        try:
            text = self.ui.util_text.toPlainText()
            type = self.ui.util_combo.currentText()

            if text:
                if type == 'decimal':
                    hex_str = " ".join(f"0x{int(num):02X}" for num in text.split())
                    self.ui.util_encode.setText(hex_str)
                    self.convertTableData(hex_str)
                elif type == 'hex':
                    self.ui.util_encode.setText('')

                elif type == 'base64':
                    byte_data = base64.b64decode(text)
                    hex_str = " ".join(f"0x{byte:02X}" for byte in byte_data)
                    self.ui.util_encode.setText(hex_str)
                    self.convertTableData(hex_str)

                elif type == 'binary':
                    byte_data = bytes(int(b, 2) for b in text.split())
                    # 바이트를 16진수 문자열로 변환
                    hex_str = " ".join(f"0x{byte:02X}" for byte in byte_data)
                    self.ui.util_encode.setText(hex_str)
                    self.convertTableData(hex_str)

                elif type == 'ascii':
                    byte_data = text.encode('utf-8')
                    hex_str = " ".join(f"0x{byte:02X}" for byte in byte_data)
                    self.ui.util_encode.setText(hex_str)
                    self.convertTableData(hex_str)
        except:
            self.ui.util_encode.setText(traceback.format_exc())


    def btnDecimal(self):
        try:
            text = self.ui.util_text.toPlainText()
            type = self.ui.util_combo.currentText()
            if text:
                if type == 'decimal':
                    self.ui.util_encode.setText('')
                elif type == 'hex':
                    decimal_str = " ".join(str(int(num, 16)) for num in text.split())
                    self.ui.util_encode.setText(decimal_str)
                    self.convertTableData(decimal_str)
                elif type =='base64':
                    byte_data = base64.b64decode(text)
                    decimal_str = " ".join(str(byte) for byte in byte_data)
                    self.ui.util_encode.setText(decimal_str)
                    self.convertTableData(decimal_str)

                elif type == 'binary':
                    byte_data = bytes(int(b, 2) for b in text.split())
                    decimal_str = " ".join(str(byte) for byte in byte_data)
                    self.ui.util_encode.setText(decimal_str)
                    self.convertTableData(decimal_str)

                elif type == 'ascii':
                    byte_data = text.encode('utf-8')
                    decimal_str = " ".join(str(byte) for byte in byte_data)
                    self.ui.util_encode.setText(decimal_str)
                    self.convertTableData(decimal_str)
        except:
            self.ui.util_encode.setText(traceback.format_exc())


    def btnBinary(self):
        try:
            text = self.ui.util_text.toPlainText()
            type = self.ui.util_combo.currentText()
            if text:
                if type == 'decimal':
                    binary_str = " ".join(f"{int(num):08b}" for num in text.split())
                    self.ui.util_encode.setText(binary_str)
                    self.convertTableData(binary_str)
                elif type == 'hex':
                    binary_str = " ".join(f"{int(num, 16):08b}" for num in text.split())
                    self.ui.util_encode.setText(binary_str)
                    self.convertTableData(binary_str)

                elif type== 'base64':
                    byte_data = base64.b64decode(text)
                    binary_str = " ".join(f"{byte:08b}" for byte in byte_data)
                    self.ui.util_encode.setText(binary_str)
                    self.convertTableData(binary_str)
                elif type == 'ascii':
                    byte_data = text.encode('utf-8')
                    binary_str = " ".join(f"{byte:08b}" for byte in byte_data)
                    self.ui.util_encode.setText(binary_str)
                    self.convertTableData(binary_str)
        except:
            self.ui.util_encode.setText(traceback.format_exc())

    def btnBase64(self):
        try:
            text = self.ui.util_text.toPlainText()
            type = self.ui.util_combo.currentText()
            if text:
                if type == 'decimal':
                    byte_data = bytes(int(num) for num in text.split())
                    base64_encoded = base64.b64encode(byte_data)
                    self.ui.util_encode.setText(base64_encoded.decode('utf-8'))
                    self.convertTableData(base64_encoded.decode('utf-8'))
                elif type =='hex':
                    byte_data = bytes(int(num, 16) for num in text.split())
                    base64_encoded = base64.b64encode(byte_data)
                    self.ui.util_encode.setText(base64_encoded.decode('utf-8'))
                    self.convertTableData(base64_encoded.decode('utf-8'))
                elif type == 'binary':
                    byte_data = bytes(int(b, 2) for b in text.split())
                    base64_encoded = base64.b64encode(byte_data)
                    self.ui.util_encode.setText(base64_encoded.decode('utf-8'))
                    self.convertTableData(base64_encoded.decode('utf-8'))
                elif type == 'ascii':
                    byte_data = text.encode('utf-8')
                    base64_encoded = base64.b64encode(byte_data)
                    self.ui.util_encode.setText(base64_encoded.decode('utf-8'))
                    self.convertTableData(base64_encoded.decode('utf-8'))
        except:
            self.ui.util_encode.setText(traceback.format_exc())

    def btnAscii(self):
        try:
            text = self.ui.util_text.toPlainText()
            type = self.ui.util_combo.currentText()
            if text:
                if type == 'decimal':
                    byte_data = bytes(int(num) for num in text.split())
                    data = byte_data.decode('utf-8', errors='replace')

                    self.ui.util_encode.setText(data)
                    self.convertTableData(" ".join(data))

                elif type == 'hex':
                    byte_data = bytes(int(num, 16) for num in text.split())
                    data = byte_data.decode('utf-8', errors='replace')
                    self.ui.util_encode.setText(data)
                    self.convertTableData(" ".join(data))

                elif type== 'base64':
                    byte_data = base64.b64decode(text)
                    data = byte_data.decode('utf-8', errors='replace')
                    self.ui.util_encode.setText(data)
                    self.convertTableData(" ".join(data))

                elif type == 'binary':
                    byte_data = bytes(int(b, 2) for b in text.split())
                    data = byte_data.decode('utf-8', errors='replace')
                    self.ui.util_encode.setText(data)
                    self.convertTableData(" ".join(data))
        except:
            self.ui.util_encode.setText(traceback.format_exc())



    def shortB(self):
        try:
            text = self.ui.util_text.toPlainText()
            type = self.ui.util_combo.currentText()
            if text:
                if type == 'decimal':
                    byte_data = bytes(int(num) for num in text.split())
                    value = int.from_bytes(byte_data, byteorder="big")
                    self.ui.util_encode.setText(str(value))
                elif type == 'hex':
                    byte_data = bytes(int(num, 16) for num in text.split())
                    value = int.from_bytes(byte_data, byteorder="big")
                    self.ui.util_encode.setText(str(value))

                elif type== 'base64':
                    byte_data = base64.b64decode(text)
                    value = int.from_bytes(byte_data, byteorder="big")
                    self.ui.util_encode.setText(str(value))
                elif type == 'binary':
                    byte_data = bytes(int(b, 2) for b in text.split())
                    value = int.from_bytes(byte_data, byteorder="big")
                    self.ui.util_encode.setText(str(value))
        except:
            self.ui.util_encode.setText(traceback.format_exc())


    def shortL(self):
        try:
            text = self.ui.util_text.toPlainText()
            type = self.ui.util_combo.currentText()
            if text:
                if type == 'decimal':
                    byte_data = bytes(int(num) for num in text.split())
                    value = int.from_bytes(byte_data, byteorder="little")
                    self.ui.util_encode.setText(str(value))
                elif type == 'hex':
                    byte_data = bytes(int(num, 16) for num in text.split())
                    value = int.from_bytes(byte_data, byteorder="little")
                    self.ui.util_encode.setText(str(value))

                elif type == 'base64':
                    byte_data = base64.b64decode(text)
                    value = int.from_bytes(byte_data, byteorder="little")
                    self.ui.util_encode.setText(str(value))

                elif type == 'binary':
                    byte_data = bytes(int(b, 2) for b in text.split())
                    value = int.from_bytes(byte_data, byteorder="little")
                    self.ui.util_encode.setText(str(value))
        except:
            self.ui.util_encode.setText(traceback.format_exc())

    def doubleB(self):
        try:
            text = self.ui.util_text.toPlainText()
            type = self.ui.util_combo.currentText()
            if text:
                if type == 'decimal':
                    byte_data = bytes(int(num) for num in text.split())
                    big_endian_value = struct.unpack(">d", byte_data)[0]
                    self.ui.util_encode.setText(str(big_endian_value))

                elif type == 'hex':
                    byte_data = bytes(int(num, 16) for num in text.split())
                    big_endian_value = struct.unpack(">d", byte_data)[0]
                    self.ui.util_encode.setText(str(big_endian_value))

                elif type == 'base64':
                    byte_data = base64.b64decode(text)
                    big_endian_value = struct.unpack(">d", byte_data)[0]
                    self.ui.util_encode.setText(str(big_endian_value))

                elif type == 'binary':
                    byte_data = bytes(int(b, 2) for b in text.split())
                    big_endian_value = struct.unpack(">d", byte_data)[0]
                    self.ui.util_encode.setText(str(big_endian_value))
        except:
            self.ui.util_encode.setText(traceback.format_exc())

    def doubleL(self):
        try:
            text = self.ui.util_text.toPlainText()
            type = self.ui.util_combo.currentText()
            if text:
                if type == 'decimal':
                    byte_data = bytes(int(num) for num in text.split())
                    big_endian_value = struct.unpack("<d", byte_data)[0]
                    self.ui.util_encode.setText(str(big_endian_value))

                elif type == 'hex':
                    byte_data = bytes(int(num, 16) for num in text.split())
                    big_endian_value = struct.unpack("<d", byte_data)[0]
                    self.ui.util_encode.setText(str(big_endian_value))

                elif type == 'base64':
                    byte_data = base64.b64decode(text)
                    big_endian_value = struct.unpack("<d", byte_data)[0]
                    self.ui.util_encode.setText(str(big_endian_value))

                elif type == 'binary':
                    byte_data = bytes(int(b, 2) for b in text.split())
                    big_endian_value = struct.unpack("<d", byte_data)[0]
                    self.ui.util_encode.setText(str(big_endian_value))
        except:
            self.ui.util_encode.setText(traceback.format_exc())


    def intB(self):
        try:
            text = self.ui.util_text.toPlainText()
            type = self.ui.util_combo.currentText()
            if text:
                if type == 'decimal':
                    byte_data = bytes(int(num) for num in text.split())
                    int_value = int.from_bytes(byte_data, byteorder="big", signed=True)
                    self.ui.util_encode.setText(str(int_value))

                elif type == 'hex':
                    byte_data = bytes(int(num, 16) for num in text.split())
                    int_value = int.from_bytes(byte_data, byteorder="big", signed=True)
                    self.ui.util_encode.setText(str(int_value))

                elif type == 'base64':
                    byte_data = base64.b64decode(text)
                    int_value = int.from_bytes(byte_data, byteorder="big", signed=True)
                    self.ui.util_encode.setText(str(int_value))

                elif type == 'binary':
                    byte_data = bytes(int(b, 2) for b in text.split())
                    int_value = int.from_bytes(byte_data, byteorder="big", signed=True)
                    self.ui.util_encode.setText(str(int_value))
        except:
            self.ui.util_encode.setText(traceback.format_exc())

    def intL(self):
        try:
            text = self.ui.util_text.toPlainText()
            type = self.ui.util_combo.currentText()
            if text:
                if type == 'decimal':
                    byte_data = bytes(int(num) for num in text.split())
                    int_value = int.from_bytes(byte_data, byteorder="little", signed=True)
                    self.ui.util_encode.setText(str(int_value))

                elif type == 'hex':
                    byte_data = bytes(int(num, 16) for num in text.split())
                    int_value = int.from_bytes(byte_data, byteorder="little", signed=True)
                    self.ui.util_encode.setText(str(int_value))

                elif type == 'base64':
                    byte_data = base64.b64decode(text)
                    int_value = int.from_bytes(byte_data, byteorder="little", signed=True)
                    self.ui.util_encode.setText(str(int_value))

                elif type == 'binary':
                    byte_data = bytes(int(b, 2) for b in text.split())
                    int_value = int.from_bytes(byte_data, byteorder="little", signed=True)
                    self.ui.util_encode.setText(str(int_value))
        except:
            self.ui.util_encode.setText(traceback.format_exc())

    def floatB(self):
        try:
            text = self.ui.util_text.toPlainText()
            type = self.ui.util_combo.currentText()
            if text:
                if type == 'decimal':
                    byte_data = bytes(int(num) for num in text.split())
                    big_endian_value = struct.unpack(">f", byte_data)[0]
                    self.ui.util_encode.setText(str(big_endian_value))

                elif type == 'hex':
                    byte_data = bytes(int(num, 16) for num in text.split())
                    big_endian_value = struct.unpack(">f", byte_data)[0]
                    self.ui.util_encode.setText(str(big_endian_value))

                elif type == 'base64':
                    byte_data = base64.b64decode(text)
                    big_endian_value = struct.unpack(">f", byte_data)[0]
                    self.ui.util_encode.setText(str(big_endian_value))

                elif type == 'binary':
                    byte_data = bytes(int(b, 2) for b in text.split())
                    big_endian_value = struct.unpack(">f", byte_data)[0]
                    self.ui.util_encode.setText(str(big_endian_value))
        except:
            self.ui.util_encode.setText(traceback.format_exc())

    def floatL(self):
        try:
            text = self.ui.util_text.toPlainText()
            type = self.ui.util_combo.currentText()
            if text:
                if type == 'decimal':
                    byte_data = bytes(int(num) for num in text.split())
                    big_endian_value = struct.unpack("<f", byte_data)[0]
                    self.ui.util_encode.setText(str(big_endian_value))

                elif type == 'hex':
                    byte_data = bytes(int(num, 16) for num in text.split())
                    big_endian_value = struct.unpack("<f", byte_data)[0]
                    self.ui.util_encode.setText(str(big_endian_value))

                elif type == 'base64':
                    byte_data = base64.b64decode(text)
                    big_endian_value = struct.unpack("<f", byte_data)[0]
                    self.ui.util_encode.setText(str(big_endian_value))

                elif type == 'binary':
                    byte_data = bytes(int(b, 2) for b in text.split())
                    big_endian_value = struct.unpack("<f", byte_data)[0]
                    self.ui.util_encode.setText(str(big_endian_value))
        except:
            self.ui.util_encode.setText(traceback.format_exc())
