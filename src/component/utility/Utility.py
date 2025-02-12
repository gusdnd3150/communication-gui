
from PySide6.QtWidgets import QTableWidgetItem, QMainWindow, QHeaderView
from PySide6.QtGui import QColor, QBrush
import sys
import os
import src.protocols.SendHandler as SendHandler

import base64

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



    def setEvent(self):
        self.ui.btn_util_hex.clicked.connect(self.btnHex)
        self.ui.btn_util_decimal.clicked.connect(self.btnDecimal)
        self.ui.btn_util_binuary.clicked.connect(self.btnBinary)
        self.ui.btn_util_base64.clicked.connect(self.btnBase64)
        self.ui.btn_util_ascii.clicked.connect(self.btnAscii)

        self.ui.util_combo.addItems(self.combos)



    def btnHex(self):
        try:
            text = self.ui.util_text.toPlainText()
            type = self.ui.util_combo.currentText()
            if text:
                if type == 'decimal':
                    hex_str = " ".join(f"0x{int(num):02X}" for num in text.split())
                    self.ui.util_encode.setText(hex_str)
                elif type == 'hex':
                    self.ui.util_encode.setText('')
                elif type == 'base64':
                    byte_data = base64.b64decode(text)
                    hex_str = " ".join(f"0x{byte:02X}" for byte in byte_data)
                    self.ui.util_encode.setText(hex_str)
                elif type == 'binary':
                    byte_data = bytes(int(b, 2) for b in text.split())
                    # 바이트를 16진수 문자열로 변환
                    hex_str = " ".join(f"0x{byte:02X}" for byte in byte_data)
                    self.ui.util_encode.setText(hex_str)
                elif type == 'ascii':
                    byte_data = text.encode('utf-8')
                    hex_str = " ".join(f"0x{byte:02X}" for byte in byte_data)
                    self.ui.util_encode.setText(hex_str)
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
                elif type =='base64':
                    byte_data = base64.b64decode(text)
                    decimal_str = " ".join(str(byte) for byte in byte_data)
                    self.ui.util_encode.setText(decimal_str)
                elif type == 'binary':
                    byte_data = bytes(int(b, 2) for b in text.split())
                    decimal_str = " ".join(str(byte) for byte in byte_data)
                    self.ui.util_encode.setText(decimal_str)
                elif type == 'ascii':
                    byte_data = text.encode('utf-8')
                    decimal_str = " ".join(str(byte) for byte in byte_data)
                    self.ui.util_encode.setText(decimal_str)
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
                elif type == 'hex':
                    binary_str = " ".join(f"{int(num, 16):08b}" for num in text.split())
                    self.ui.util_encode.setText(binary_str)
                elif type== 'base64':
                    byte_data = base64.b64decode(text)
                    binary_str = " ".join(f"{byte:08b}" for byte in byte_data)
                    self.ui.util_encode.setText(binary_str)
                elif type == 'ascii':
                    byte_data = text.encode('utf-8')
                    binary_str = " ".join(f"{byte:08b}" for byte in byte_data)
                    self.ui.util_encode.setText(binary_str)
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
                elif type =='hex':
                    byte_data = bytes(int(num, 16) for num in text.split())
                    base64_encoded = base64.b64encode(byte_data)
                    self.ui.util_encode.setText(base64_encoded.decode('utf-8'))
                elif type == 'binary':
                    byte_data = bytes(int(b, 2) for b in text.split())
                    base64_encoded = base64.b64encode(byte_data)
                    self.ui.util_encode.setText(base64_encoded.decode('utf-8'))
                elif type == 'ascii':
                    byte_data = text.encode('utf-8')
                    base64_encoded = base64.b64encode(byte_data)
                    self.ui.util_encode.setText(base64_encoded.decode('utf-8'))
        except:
            self.ui.util_encode.setText(traceback.format_exc())

    def btnAscii(self):
        try:
            text = self.ui.util_text.toPlainText()
            type = self.ui.util_combo.currentText()
            if text:
                if type == 'decimal':
                    byte_data = bytes(int(num) for num in text.split())
                    self.ui.util_encode.setText(byte_data.decode('utf-8'))
                elif type == 'hex':
                    byte_data = bytes(int(num, 16) for num in text.split())
                    self.ui.util_encode.setText(byte_data.decode('utf-8'))

                elif type== 'base64':
                    byte_data = base64.b64decode(text)
                    self.ui.util_encode.setText(byte_data.decode('utf-8'))
                elif type == 'binary':
                    byte_data = bytes(int(b, 2) for b in text.split())
                    self.ui.util_encode.setText(byte_data.decode('utf-8'))
        except:
            self.ui.util_encode.setText(traceback.format_exc())