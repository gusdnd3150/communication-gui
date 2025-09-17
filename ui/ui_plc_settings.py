# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'plc_settings.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QFormLayout,
    QFrame, QGridLayout, QHeaderView, QLabel,
    QLineEdit, QMainWindow, QMenuBar, QSizePolicy,
    QStatusBar, QTabWidget, QTableWidget, QTableWidgetItem,
    QToolButton, QWidget)

class Ui_PLC_Settings(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1150, 600)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(1150, 600))
        MainWindow.setMaximumSize(QSize(1150, 600))
        MainWindow.setBaseSize(QSize(600, 300))
        font = QFont()
        font.setFamilies([u"\ub9d1\uc740 \uace0\ub515"])
        font.setBold(True)
        MainWindow.setFont(font)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_2.addWidget(self.line, 1, 1, 1, 1)

        self.tap_info = QTabWidget(self.centralwidget)
        self.tap_info.setObjectName(u"tap_info")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.layoutWidget = QWidget(self.tab)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(810, 0, 155, 28))
        self.gridLayout = QGridLayout(self.layoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.btn_addPlc = QToolButton(self.layoutWidget)
        self.btn_addPlc.setObjectName(u"btn_addPlc")

        self.gridLayout.addWidget(self.btn_addPlc, 0, 0, 1, 1)

        self.btn_delPlc = QToolButton(self.layoutWidget)
        self.btn_delPlc.setObjectName(u"btn_delPlc")

        self.gridLayout.addWidget(self.btn_delPlc, 0, 2, 1, 1)

        self.btn_savePlc = QToolButton(self.layoutWidget)
        self.btn_savePlc.setObjectName(u"btn_savePlc")

        self.gridLayout.addWidget(self.btn_savePlc, 0, 1, 1, 1)

        self.formLayoutWidget_2 = QWidget(self.tab)
        self.formLayoutWidget_2.setObjectName(u"formLayoutWidget_2")
        self.formLayoutWidget_2.setGeometry(QRect(810, 30, 271, 461))
        self.formLayout_2 = QFormLayout(self.formLayoutWidget_2)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_7 = QLabel(self.formLayoutWidget_2)
        self.label_7.setObjectName(u"label_7")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_7)

        self.PLC_PKG_ID = QLineEdit(self.formLayoutWidget_2)
        self.PLC_PKG_ID.setObjectName(u"PLC_PKG_ID")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.FieldRole, self.PLC_PKG_ID)

        self.label_8 = QLabel(self.formLayoutWidget_2)
        self.label_8.setObjectName(u"label_8")

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_8)

        self.PLC_PLC_ID = QLineEdit(self.formLayoutWidget_2)
        self.PLC_PLC_ID.setObjectName(u"PLC_PLC_ID")

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.FieldRole, self.PLC_PLC_ID)

        self.label_9 = QLabel(self.formLayoutWidget_2)
        self.label_9.setObjectName(u"label_9")

        self.formLayout_2.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_9)

        self.PLC_PLC_MAKER = QComboBox(self.formLayoutWidget_2)
        self.PLC_PLC_MAKER.setObjectName(u"PLC_PLC_MAKER")

        self.formLayout_2.setWidget(3, QFormLayout.ItemRole.FieldRole, self.PLC_PLC_MAKER)

        self.label_12 = QLabel(self.formLayoutWidget_2)
        self.label_12.setObjectName(u"label_12")

        self.formLayout_2.setWidget(4, QFormLayout.ItemRole.LabelRole, self.label_12)

        self.PLC_CPU_TY = QComboBox(self.formLayoutWidget_2)
        self.PLC_CPU_TY.setObjectName(u"PLC_CPU_TY")

        self.formLayout_2.setWidget(4, QFormLayout.ItemRole.FieldRole, self.PLC_CPU_TY)

        self.label_13 = QLabel(self.formLayoutWidget_2)
        self.label_13.setObjectName(u"label_13")

        self.formLayout_2.setWidget(5, QFormLayout.ItemRole.LabelRole, self.label_13)

        self.PLC_SLOT = QComboBox(self.formLayoutWidget_2)
        self.PLC_SLOT.setObjectName(u"PLC_SLOT")

        self.formLayout_2.setWidget(5, QFormLayout.ItemRole.FieldRole, self.PLC_SLOT)

        self.label_14 = QLabel(self.formLayoutWidget_2)
        self.label_14.setObjectName(u"label_14")

        self.formLayout_2.setWidget(6, QFormLayout.ItemRole.LabelRole, self.label_14)

        self.PLC_RACK = QComboBox(self.formLayoutWidget_2)
        self.PLC_RACK.setObjectName(u"PLC_RACK")

        self.formLayout_2.setWidget(6, QFormLayout.ItemRole.FieldRole, self.PLC_RACK)

        self.label_18 = QLabel(self.formLayoutWidget_2)
        self.label_18.setObjectName(u"label_18")

        self.formLayout_2.setWidget(7, QFormLayout.ItemRole.LabelRole, self.label_18)

        self.PLC_COMM_TY = QComboBox(self.formLayoutWidget_2)
        self.PLC_COMM_TY.setObjectName(u"PLC_COMM_TY")

        self.formLayout_2.setWidget(7, QFormLayout.ItemRole.FieldRole, self.PLC_COMM_TY)

        self.label_16 = QLabel(self.formLayoutWidget_2)
        self.label_16.setObjectName(u"label_16")

        self.formLayout_2.setWidget(8, QFormLayout.ItemRole.LabelRole, self.label_16)

        self.PLC_PLC_IP = QLineEdit(self.formLayoutWidget_2)
        self.PLC_PLC_IP.setObjectName(u"PLC_PLC_IP")

        self.formLayout_2.setWidget(8, QFormLayout.ItemRole.FieldRole, self.PLC_PLC_IP)

        self.label_15 = QLabel(self.formLayoutWidget_2)
        self.label_15.setObjectName(u"label_15")

        self.formLayout_2.setWidget(9, QFormLayout.ItemRole.LabelRole, self.label_15)

        self.PLC_PLC_PORT = QLineEdit(self.formLayoutWidget_2)
        self.PLC_PLC_PORT.setObjectName(u"PLC_PLC_PORT")

        self.formLayout_2.setWidget(9, QFormLayout.ItemRole.FieldRole, self.PLC_PLC_PORT)

        self.label_11 = QLabel(self.formLayoutWidget_2)
        self.label_11.setObjectName(u"label_11")

        self.formLayout_2.setWidget(10, QFormLayout.ItemRole.LabelRole, self.label_11)

        self.PLC_LOG_YN = QComboBox(self.formLayoutWidget_2)
        self.PLC_LOG_YN.setObjectName(u"PLC_LOG_YN")

        self.formLayout_2.setWidget(10, QFormLayout.ItemRole.FieldRole, self.PLC_LOG_YN)

        self.PLC_USE_YN = QComboBox(self.formLayoutWidget_2)
        self.PLC_USE_YN.setObjectName(u"PLC_USE_YN")

        self.formLayout_2.setWidget(2, QFormLayout.ItemRole.FieldRole, self.PLC_USE_YN)

        self.label_10 = QLabel(self.formLayoutWidget_2)
        self.label_10.setObjectName(u"label_10")

        self.formLayout_2.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_10)

        self.list_plc = QTableWidget(self.tab)
        if (self.list_plc.columnCount() < 1):
            self.list_plc.setColumnCount(1)
        __qtablewidgetitem = QTableWidgetItem()
        self.list_plc.setHorizontalHeaderItem(0, __qtablewidgetitem)
        self.list_plc.setObjectName(u"list_plc")
        self.list_plc.setGeometry(QRect(0, 40, 801, 451))
        font1 = QFont()
        font1.setFamilies([u"\ub9d1\uc740 \uace0\ub515"])
        font1.setPointSize(9)
        font1.setBold(True)
        self.list_plc.setFont(font1)
        self.list_plc.setProperty(u"showDropIndicator", False)
        self.list_plc.setDragEnabled(False)
        self.list_plc.setDragDropOverwriteMode(False)
        self.list_plc.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.label_4 = QLabel(self.tab)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(10, 10, 53, 22))
        self.plc_search_pkg = QLineEdit(self.tab)
        self.plc_search_pkg.setObjectName(u"plc_search_pkg")
        self.plc_search_pkg.setGeometry(QRect(50, 10, 71, 22))
        self.label_5 = QLabel(self.tab)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(130, 10, 51, 22))
        self.plc_search_plc = QLineEdit(self.tab)
        self.plc_search_plc.setObjectName(u"plc_search_plc")
        self.plc_search_plc.setGeometry(QRect(190, 10, 111, 22))
        self.tap_info.addTab(self.tab, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.selected_msg = QLabel(self.tab_3)
        self.selected_msg.setObjectName(u"selected_msg")
        self.selected_msg.setGeometry(QRect(650, 20, 281, 16))
        self.label_6 = QLabel(self.tab_3)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(10, 10, 53, 22))
        self.formLayoutWidget_3 = QWidget(self.tab_3)
        self.formLayoutWidget_3.setObjectName(u"formLayoutWidget_3")
        self.formLayoutWidget_3.setGeometry(QRect(810, 30, 271, 461))
        self.formLayout_3 = QFormLayout(self.formLayoutWidget_3)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.formLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_17 = QLabel(self.formLayoutWidget_3)
        self.label_17.setObjectName(u"label_17")

        self.formLayout_3.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_17)

        self.READ_PKG_ID = QLineEdit(self.formLayoutWidget_3)
        self.READ_PKG_ID.setObjectName(u"READ_PKG_ID")

        self.formLayout_3.setWidget(0, QFormLayout.ItemRole.FieldRole, self.READ_PKG_ID)

        self.label_19 = QLabel(self.formLayoutWidget_3)
        self.label_19.setObjectName(u"label_19")

        self.formLayout_3.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_19)

        self.READ_PLC_ID = QLineEdit(self.formLayoutWidget_3)
        self.READ_PLC_ID.setObjectName(u"READ_PLC_ID")

        self.formLayout_3.setWidget(1, QFormLayout.ItemRole.FieldRole, self.READ_PLC_ID)

        self.label_28 = QLabel(self.formLayoutWidget_3)
        self.label_28.setObjectName(u"label_28")

        self.formLayout_3.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_28)

        self.READ_USE_YN = QComboBox(self.formLayoutWidget_3)
        self.READ_USE_YN.setObjectName(u"READ_USE_YN")

        self.formLayout_3.setWidget(2, QFormLayout.ItemRole.FieldRole, self.READ_USE_YN)

        self.label_20 = QLabel(self.formLayoutWidget_3)
        self.label_20.setObjectName(u"label_20")

        self.formLayout_3.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_20)

        self.READ_ADDR = QLineEdit(self.formLayoutWidget_3)
        self.READ_ADDR.setObjectName(u"READ_ADDR")

        self.formLayout_3.setWidget(3, QFormLayout.ItemRole.FieldRole, self.READ_ADDR)

        self.label_21 = QLabel(self.formLayoutWidget_3)
        self.label_21.setObjectName(u"label_21")

        self.formLayout_3.setWidget(4, QFormLayout.ItemRole.LabelRole, self.label_21)

        self.READ_POS = QLineEdit(self.formLayoutWidget_3)
        self.READ_POS.setObjectName(u"READ_POS")

        self.formLayout_3.setWidget(4, QFormLayout.ItemRole.FieldRole, self.READ_POS)

        self.label_22 = QLabel(self.formLayoutWidget_3)
        self.label_22.setObjectName(u"label_22")

        self.formLayout_3.setWidget(5, QFormLayout.ItemRole.LabelRole, self.label_22)

        self.READ_LENGTH = QLineEdit(self.formLayoutWidget_3)
        self.READ_LENGTH.setObjectName(u"READ_LENGTH")

        self.formLayout_3.setWidget(5, QFormLayout.ItemRole.FieldRole, self.READ_LENGTH)

        self.label_23 = QLabel(self.formLayoutWidget_3)
        self.label_23.setObjectName(u"label_23")

        self.formLayout_3.setWidget(6, QFormLayout.ItemRole.LabelRole, self.label_23)

        self.READ_ALIAS = QLineEdit(self.formLayoutWidget_3)
        self.READ_ALIAS.setObjectName(u"READ_ALIAS")

        self.formLayout_3.setWidget(6, QFormLayout.ItemRole.FieldRole, self.READ_ALIAS)

        self.addr_search_pkg = QLineEdit(self.tab_3)
        self.addr_search_pkg.setObjectName(u"addr_search_pkg")
        self.addr_search_pkg.setGeometry(QRect(50, 10, 71, 22))
        self.label_29 = QLabel(self.tab_3)
        self.label_29.setObjectName(u"label_29")
        self.label_29.setGeometry(QRect(130, 10, 51, 22))
        self.list_addr = QTableWidget(self.tab_3)
        if (self.list_addr.columnCount() < 1):
            self.list_addr.setColumnCount(1)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.list_addr.setHorizontalHeaderItem(0, __qtablewidgetitem1)
        self.list_addr.setObjectName(u"list_addr")
        self.list_addr.setGeometry(QRect(0, 40, 801, 451))
        self.list_addr.setFont(font1)
        self.list_addr.setProperty(u"showDropIndicator", False)
        self.list_addr.setDragEnabled(False)
        self.list_addr.setDragDropOverwriteMode(False)
        self.list_addr.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.addr_search_plc = QLineEdit(self.tab_3)
        self.addr_search_plc.setObjectName(u"addr_search_plc")
        self.addr_search_plc.setGeometry(QRect(190, 10, 111, 22))
        self.layoutWidget_2 = QWidget(self.tab_3)
        self.layoutWidget_2.setObjectName(u"layoutWidget_2")
        self.layoutWidget_2.setGeometry(QRect(810, 0, 155, 28))
        self.gridLayout_3 = QGridLayout(self.layoutWidget_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.btn_addAddr = QToolButton(self.layoutWidget_2)
        self.btn_addAddr.setObjectName(u"btn_addAddr")

        self.gridLayout_3.addWidget(self.btn_addAddr, 0, 0, 1, 1)

        self.btn_delAddr = QToolButton(self.layoutWidget_2)
        self.btn_delAddr.setObjectName(u"btn_delAddr")

        self.gridLayout_3.addWidget(self.btn_delAddr, 0, 2, 1, 1)

        self.btn_saveAddr = QToolButton(self.layoutWidget_2)
        self.btn_saveAddr.setObjectName(u"btn_saveAddr")

        self.gridLayout_3.addWidget(self.btn_saveAddr, 0, 1, 1, 1)

        self.tap_info.addTab(self.tab_3, "")

        self.gridLayout_2.addWidget(self.tap_info, 2, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1150, 26))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tap_info.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.btn_addPlc.setText(QCoreApplication.translate("MainWindow", u"\uc2e0\uaddc", None))
        self.btn_delPlc.setText(QCoreApplication.translate("MainWindow", u"\uc0ad\uc81c", None))
        self.btn_savePlc.setText(QCoreApplication.translate("MainWindow", u"\uc800\uc7a5", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\ud328\ud0a4\uc9c0 \uba85", None))
        self.PLC_PKG_ID.setText("")
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"PLC \uc544\uc774\ub514", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"MAKER", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"CPU Type", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Slot", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Rack", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"\ud1b5\uc2e0\ud0c0\uc785", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"\uc544\uc774\ud53c", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"\ud3ec\ud2b8", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"\ub85c\uadf8 \ucd9c\ub825", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"\uc0ac\uc6a9\uc5ec\ubd80", None))
        ___qtablewidgetitem = self.list_plc.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"\uc0c8 \ud589", None));
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"PKG", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"PLC id", None))
        self.tap_info.setTabText(self.tap_info.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"PLC", None))
        self.selected_msg.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"PKG", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"\ud328\ud0a4\uc9c0 \uba85", None))
        self.READ_PKG_ID.setText("")
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"PLC \uc544\uc774\ub514", None))
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"\uc0ac\uc6a9\uc5ec\ubd80", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"Address", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"Pos", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"Length", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"Alias", None))
        self.label_29.setText(QCoreApplication.translate("MainWindow", u"PLC id", None))
        ___qtablewidgetitem1 = self.list_addr.horizontalHeaderItem(0)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"\uc0c8 \ud589", None));
        self.btn_addAddr.setText(QCoreApplication.translate("MainWindow", u"\uc2e0\uaddc", None))
        self.btn_delAddr.setText(QCoreApplication.translate("MainWindow", u"\uc0ad\uc81c", None))
        self.btn_saveAddr.setText(QCoreApplication.translate("MainWindow", u"\uc800\uc7a5", None))
        self.tap_info.setTabText(self.tap_info.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"READ address", None))
    # retranslateUi

