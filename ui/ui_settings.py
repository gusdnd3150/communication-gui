# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
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
    QLineEdit, QMainWindow, QMenuBar, QPushButton,
    QSizePolicy, QStatusBar, QTabWidget, QTableWidget,
    QTableWidgetItem, QTextEdit, QToolButton, QWidget)

class Ui_Settings(object):
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
        self.line.setFrameShape(QFrame.Shape.HLine)
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
        self.btn_addSk = QToolButton(self.layoutWidget)
        self.btn_addSk.setObjectName(u"btn_addSk")

        self.gridLayout.addWidget(self.btn_addSk, 0, 0, 1, 1)

        self.btn_delSk = QToolButton(self.layoutWidget)
        self.btn_delSk.setObjectName(u"btn_delSk")

        self.gridLayout.addWidget(self.btn_delSk, 0, 2, 1, 1)

        self.btn_saveSk = QToolButton(self.layoutWidget)
        self.btn_saveSk.setObjectName(u"btn_saveSk")

        self.gridLayout.addWidget(self.btn_saveSk, 0, 1, 1, 1)

        self.formLayoutWidget_2 = QWidget(self.tab)
        self.formLayoutWidget_2.setObjectName(u"formLayoutWidget_2")
        self.formLayoutWidget_2.setGeometry(QRect(810, 30, 271, 473))
        self.formLayout_2 = QFormLayout(self.formLayoutWidget_2)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_7 = QLabel(self.formLayoutWidget_2)
        self.label_7.setObjectName(u"label_7")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_7)

        self.sk_PKG_ID = QLineEdit(self.formLayoutWidget_2)
        self.sk_PKG_ID.setObjectName(u"sk_PKG_ID")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.sk_PKG_ID)

        self.label_8 = QLabel(self.formLayoutWidget_2)
        self.label_8.setObjectName(u"label_8")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_8)

        self.sk_SK_ID = QLineEdit(self.formLayoutWidget_2)
        self.sk_SK_ID.setObjectName(u"sk_SK_ID")

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.sk_SK_ID)

        self.label_9 = QLabel(self.formLayoutWidget_2)
        self.label_9.setObjectName(u"label_9")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.label_9)

        self.label_10 = QLabel(self.formLayoutWidget_2)
        self.label_10.setObjectName(u"label_10")

        self.formLayout_2.setWidget(12, QFormLayout.LabelRole, self.label_10)

        self.label_11 = QLabel(self.formLayoutWidget_2)
        self.label_11.setObjectName(u"label_11")

        self.formLayout_2.setWidget(11, QFormLayout.LabelRole, self.label_11)

        self.label_12 = QLabel(self.formLayoutWidget_2)
        self.label_12.setObjectName(u"label_12")

        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.label_12)

        self.label_13 = QLabel(self.formLayoutWidget_2)
        self.label_13.setObjectName(u"label_13")

        self.formLayout_2.setWidget(4, QFormLayout.LabelRole, self.label_13)

        self.label_14 = QLabel(self.formLayoutWidget_2)
        self.label_14.setObjectName(u"label_14")

        self.formLayout_2.setWidget(10, QFormLayout.LabelRole, self.label_14)

        self.label_15 = QLabel(self.formLayoutWidget_2)
        self.label_15.setObjectName(u"label_15")

        self.formLayout_2.setWidget(9, QFormLayout.LabelRole, self.label_15)

        self.label_16 = QLabel(self.formLayoutWidget_2)
        self.label_16.setObjectName(u"label_16")

        self.formLayout_2.setWidget(8, QFormLayout.LabelRole, self.label_16)

        self.label_17 = QLabel(self.formLayoutWidget_2)
        self.label_17.setObjectName(u"label_17")

        self.formLayout_2.setWidget(7, QFormLayout.LabelRole, self.label_17)

        self.label_18 = QLabel(self.formLayoutWidget_2)
        self.label_18.setObjectName(u"label_18")

        self.formLayout_2.setWidget(5, QFormLayout.LabelRole, self.label_18)

        self.label_19 = QLabel(self.formLayoutWidget_2)
        self.label_19.setObjectName(u"label_19")

        self.formLayout_2.setWidget(6, QFormLayout.LabelRole, self.label_19)

        self.sk_SK_GROUP = QLineEdit(self.formLayoutWidget_2)
        self.sk_SK_GROUP.setObjectName(u"sk_SK_GROUP")

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.sk_SK_GROUP)

        self.sk_SK_IP = QLineEdit(self.formLayoutWidget_2)
        self.sk_SK_IP.setObjectName(u"sk_SK_IP")

        self.formLayout_2.setWidget(8, QFormLayout.FieldRole, self.sk_SK_IP)

        self.sk_SK_PORT = QLineEdit(self.formLayoutWidget_2)
        self.sk_SK_PORT.setObjectName(u"sk_SK_PORT")

        self.formLayout_2.setWidget(9, QFormLayout.FieldRole, self.sk_SK_PORT)

        self.sk_SK_DELIMIT_TYPE = QLineEdit(self.formLayoutWidget_2)
        self.sk_SK_DELIMIT_TYPE.setObjectName(u"sk_SK_DELIMIT_TYPE")

        self.formLayout_2.setWidget(10, QFormLayout.FieldRole, self.sk_SK_DELIMIT_TYPE)

        self.sk_USE_YN = QComboBox(self.formLayoutWidget_2)
        self.sk_USE_YN.setObjectName(u"sk_USE_YN")

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.sk_USE_YN)

        self.sk_SK_TYPE = QComboBox(self.formLayoutWidget_2)
        self.sk_SK_TYPE.setObjectName(u"sk_SK_TYPE")

        self.formLayout_2.setWidget(4, QFormLayout.FieldRole, self.sk_SK_TYPE)

        self.sk_SK_CONN_TYPE = QComboBox(self.formLayoutWidget_2)
        self.sk_SK_CONN_TYPE.setObjectName(u"sk_SK_CONN_TYPE")

        self.formLayout_2.setWidget(5, QFormLayout.FieldRole, self.sk_SK_CONN_TYPE)

        self.sk_SK_CLIENT_TYPE = QComboBox(self.formLayoutWidget_2)
        self.sk_SK_CLIENT_TYPE.setObjectName(u"sk_SK_CLIENT_TYPE")

        self.formLayout_2.setWidget(6, QFormLayout.FieldRole, self.sk_SK_CLIENT_TYPE)

        self.sk_HD_ID = QComboBox(self.formLayoutWidget_2)
        self.sk_HD_ID.setObjectName(u"sk_HD_ID")

        self.formLayout_2.setWidget(7, QFormLayout.FieldRole, self.sk_HD_ID)

        self.sk_SK_LOG = QComboBox(self.formLayoutWidget_2)
        self.sk_SK_LOG.setObjectName(u"sk_SK_LOG")

        self.formLayout_2.setWidget(11, QFormLayout.FieldRole, self.sk_SK_LOG)

        self.sk_SK_DESC = QTextEdit(self.formLayoutWidget_2)
        self.sk_SK_DESC.setObjectName(u"sk_SK_DESC")

        self.formLayout_2.setWidget(12, QFormLayout.FieldRole, self.sk_SK_DESC)

        self.list_sk = QTableWidget(self.tab)
        if (self.list_sk.columnCount() < 1):
            self.list_sk.setColumnCount(1)
        __qtablewidgetitem = QTableWidgetItem()
        self.list_sk.setHorizontalHeaderItem(0, __qtablewidgetitem)
        self.list_sk.setObjectName(u"list_sk")
        self.list_sk.setGeometry(QRect(0, 0, 801, 501))
        font1 = QFont()
        font1.setFamilies([u"\ub9d1\uc740 \uace0\ub515"])
        font1.setPointSize(7)
        font1.setBold(True)
        self.list_sk.setFont(font1)
        self.list_sk.setProperty("showDropIndicator", False)
        self.list_sk.setDragEnabled(False)
        self.list_sk.setDragDropOverwriteMode(False)
        self.list_sk.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tap_info.addTab(self.tab, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.list_in = QTableWidget(self.tab_5)
        if (self.list_in.columnCount() < 1):
            self.list_in.setColumnCount(1)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.list_in.setHorizontalHeaderItem(0, __qtablewidgetitem1)
        self.list_in.setObjectName(u"list_in")
        self.list_in.setGeometry(QRect(0, 0, 801, 501))
        self.list_in.setFont(font1)
        self.list_in.setTabKeyNavigation(False)
        self.list_in.setProperty("showDropIndicator", False)
        self.list_in.setDragDropOverwriteMode(False)
        self.list_in.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.formLayoutWidget_4 = QWidget(self.tab_5)
        self.formLayoutWidget_4.setObjectName(u"formLayoutWidget_4")
        self.formLayoutWidget_4.setGeometry(QRect(810, 30, 271, 461))
        self.formLayout_4 = QFormLayout(self.formLayoutWidget_4)
        self.formLayout_4.setObjectName(u"formLayout_4")
        self.formLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_20 = QLabel(self.formLayoutWidget_4)
        self.label_20.setObjectName(u"label_20")

        self.formLayout_4.setWidget(0, QFormLayout.LabelRole, self.label_20)

        self.in_PKG_ID = QLineEdit(self.formLayoutWidget_4)
        self.in_PKG_ID.setObjectName(u"in_PKG_ID")

        self.formLayout_4.setWidget(0, QFormLayout.FieldRole, self.in_PKG_ID)

        self.label_21 = QLabel(self.formLayoutWidget_4)
        self.label_21.setObjectName(u"label_21")

        self.formLayout_4.setWidget(1, QFormLayout.LabelRole, self.label_21)

        self.in_IN_SK_ID = QLineEdit(self.formLayoutWidget_4)
        self.in_IN_SK_ID.setObjectName(u"in_IN_SK_ID")

        self.formLayout_4.setWidget(1, QFormLayout.FieldRole, self.in_IN_SK_ID)

        self.label_22 = QLabel(self.formLayoutWidget_4)
        self.label_22.setObjectName(u"label_22")

        self.formLayout_4.setWidget(3, QFormLayout.LabelRole, self.label_22)

        self.in_IN_MSG_ID = QLineEdit(self.formLayoutWidget_4)
        self.in_IN_MSG_ID.setObjectName(u"in_IN_MSG_ID")

        self.formLayout_4.setWidget(3, QFormLayout.FieldRole, self.in_IN_MSG_ID)

        self.label_24 = QLabel(self.formLayoutWidget_4)
        self.label_24.setObjectName(u"label_24")

        self.formLayout_4.setWidget(4, QFormLayout.LabelRole, self.label_24)

        self.in_BZ_METHOD = QLineEdit(self.formLayoutWidget_4)
        self.in_BZ_METHOD.setObjectName(u"in_BZ_METHOD")

        self.formLayout_4.setWidget(4, QFormLayout.FieldRole, self.in_BZ_METHOD)

        self.label_25 = QLabel(self.formLayoutWidget_4)
        self.label_25.setObjectName(u"label_25")

        self.formLayout_4.setWidget(5, QFormLayout.LabelRole, self.label_25)

        self.in_USE_YN = QComboBox(self.formLayoutWidget_4)
        self.in_USE_YN.setObjectName(u"in_USE_YN")

        self.formLayout_4.setWidget(5, QFormLayout.FieldRole, self.in_USE_YN)

        self.label_23 = QLabel(self.formLayoutWidget_4)
        self.label_23.setObjectName(u"label_23")

        self.formLayout_4.setWidget(6, QFormLayout.LabelRole, self.label_23)

        self.in_IN_DESC = QTextEdit(self.formLayoutWidget_4)
        self.in_IN_DESC.setObjectName(u"in_IN_DESC")

        self.formLayout_4.setWidget(6, QFormLayout.FieldRole, self.in_IN_DESC)

        self.ss = QLabel(self.formLayoutWidget_4)
        self.ss.setObjectName(u"ss")

        self.formLayout_4.setWidget(2, QFormLayout.LabelRole, self.ss)

        self.in_SK_IN_SEQ = QLineEdit(self.formLayoutWidget_4)
        self.in_SK_IN_SEQ.setObjectName(u"in_SK_IN_SEQ")

        self.formLayout_4.setWidget(2, QFormLayout.FieldRole, self.in_SK_IN_SEQ)

        self.layoutWidget_2 = QWidget(self.tab_5)
        self.layoutWidget_2.setObjectName(u"layoutWidget_2")
        self.layoutWidget_2.setGeometry(QRect(810, 0, 155, 28))
        self.gridLayout_3 = QGridLayout(self.layoutWidget_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.btn_addIn = QToolButton(self.layoutWidget_2)
        self.btn_addIn.setObjectName(u"btn_addIn")

        self.gridLayout_3.addWidget(self.btn_addIn, 0, 0, 1, 1)

        self.btn_delIn = QToolButton(self.layoutWidget_2)
        self.btn_delIn.setObjectName(u"btn_delIn")

        self.gridLayout_3.addWidget(self.btn_delIn, 0, 2, 1, 1)

        self.btn_saveIn = QToolButton(self.layoutWidget_2)
        self.btn_saveIn.setObjectName(u"btn_saveIn")

        self.gridLayout_3.addWidget(self.btn_saveIn, 0, 1, 1, 1)

        self.tap_info.addTab(self.tab_5, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.formLayoutWidget = QWidget(self.tab_3)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(9, 9, 140, 31))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.formLayoutWidget)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.msg_MSG_ID_iq = QLineEdit(self.formLayoutWidget)
        self.msg_MSG_ID_iq.setObjectName(u"msg_MSG_ID_iq")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.msg_MSG_ID_iq)

        self.msg_search = QPushButton(self.tab_3)
        self.msg_search.setObjectName(u"msg_search")
        self.msg_search.setGeometry(QRect(999, 10, 111, 23))
        self.formLayoutWidget_3 = QWidget(self.tab_3)
        self.formLayoutWidget_3.setObjectName(u"formLayoutWidget_3")
        self.formLayoutWidget_3.setGeometry(QRect(150, 10, 140, 30))
        self.formLayout_3 = QFormLayout(self.formLayoutWidget_3)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.formLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.formLayoutWidget_3)
        self.label_2.setObjectName(u"label_2")

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.label_2)

        self.msg_MSG_MID_iq = QLineEdit(self.formLayoutWidget_3)
        self.msg_MSG_MID_iq.setObjectName(u"msg_MSG_MID_iq")

        self.formLayout_3.setWidget(0, QFormLayout.FieldRole, self.msg_MSG_MID_iq)

        self.msg_add = QPushButton(self.tab_3)
        self.msg_add.setObjectName(u"msg_add")
        self.msg_add.setGeometry(QRect(10, 50, 75, 23))
        self.msg_list = QTableWidget(self.tab_3)
        self.msg_list.setObjectName(u"msg_list")
        self.msg_list.setGeometry(QRect(10, 80, 511, 411))
        self.msg_list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.msg_list.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.msg_list.setSortingEnabled(True)
        self.msg_dt_list = QTableWidget(self.tab_3)
        self.msg_dt_list.setObjectName(u"msg_dt_list")
        self.msg_dt_list.setGeometry(QRect(580, 80, 531, 411))
        self.msg_dt_list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.msg_dt_list.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.msg_dt_add = QPushButton(self.tab_3)
        self.msg_dt_add.setObjectName(u"msg_dt_add")
        self.msg_dt_add.setGeometry(QRect(580, 50, 75, 23))
        self.msg_dt_del = QPushButton(self.tab_3)
        self.msg_dt_del.setObjectName(u"msg_dt_del")
        self.msg_dt_del.setGeometry(QRect(670, 50, 75, 23))
        self.msg_del = QPushButton(self.tab_3)
        self.msg_del.setObjectName(u"msg_del")
        self.msg_del.setGeometry(QRect(100, 50, 75, 23))
        self.line_2 = QFrame(self.tab_3)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setGeometry(QRect(540, 90, 20, 401))
        self.line_2.setFrameShape(QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)
        self.msg_save = QPushButton(self.tab_3)
        self.msg_save.setObjectName(u"msg_save")
        self.msg_save.setGeometry(QRect(190, 50, 75, 23))
        self.msg_dt_save = QPushButton(self.tab_3)
        self.msg_dt_save.setObjectName(u"msg_dt_save")
        self.msg_dt_save.setGeometry(QRect(760, 50, 75, 23))
        self.label_3 = QLabel(self.tab_3)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(590, 20, 61, 16))
        self.selected_msg = QLabel(self.tab_3)
        self.selected_msg.setObjectName(u"selected_msg")
        self.selected_msg.setGeometry(QRect(650, 20, 281, 16))
        self.tap_info.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.label_6 = QLabel(self.tab_4)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(9, 9, 101, 16))
        self.label_5 = QLabel(self.tab_4)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(10, 260, 104, 16))
        self.list_bz = QTableWidget(self.tab_4)
        if (self.list_bz.columnCount() < 1):
            self.list_bz.setColumnCount(1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.list_bz.setHorizontalHeaderItem(0, __qtablewidgetitem2)
        self.list_bz.setObjectName(u"list_bz")
        self.list_bz.setGeometry(QRect(10, 30, 821, 211))
        self.list_bz.setFont(font1)
        self.list_bz.setDragEnabled(True)
        self.list_bz.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.list_sch = QTableWidget(self.tab_4)
        if (self.list_sch.columnCount() < 1):
            self.list_sch.setColumnCount(1)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.list_sch.setHorizontalHeaderItem(0, __qtablewidgetitem3)
        self.list_sch.setObjectName(u"list_sch")
        self.list_sch.setGeometry(QRect(10, 280, 821, 211))
        self.list_sch.setFont(font1)
        self.list_sch.setDragEnabled(True)
        self.list_sch.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.formLayoutWidget_5 = QWidget(self.tab_4)
        self.formLayoutWidget_5.setObjectName(u"formLayoutWidget_5")
        self.formLayoutWidget_5.setGeometry(QRect(840, 60, 271, 281))
        self.formLayout_5 = QFormLayout(self.formLayoutWidget_5)
        self.formLayout_5.setObjectName(u"formLayout_5")
        self.formLayout_5.setContentsMargins(0, 0, 0, 0)
        self.label_26 = QLabel(self.formLayoutWidget_5)
        self.label_26.setObjectName(u"label_26")

        self.formLayout_5.setWidget(0, QFormLayout.LabelRole, self.label_26)

        self.bz_PKG_ID = QLineEdit(self.formLayoutWidget_5)
        self.bz_PKG_ID.setObjectName(u"bz_PKG_ID")

        self.formLayout_5.setWidget(0, QFormLayout.FieldRole, self.bz_PKG_ID)

        self.label_27 = QLabel(self.formLayoutWidget_5)
        self.label_27.setObjectName(u"label_27")

        self.formLayout_5.setWidget(1, QFormLayout.LabelRole, self.label_27)

        self.bz_SK_GROUP = QLineEdit(self.formLayoutWidget_5)
        self.bz_SK_GROUP.setObjectName(u"bz_SK_GROUP")

        self.formLayout_5.setWidget(1, QFormLayout.FieldRole, self.bz_SK_GROUP)

        self.ss_2 = QLabel(self.formLayoutWidget_5)
        self.ss_2.setObjectName(u"ss_2")

        self.formLayout_5.setWidget(2, QFormLayout.LabelRole, self.ss_2)

        self.bz_BZ_TYPE = QComboBox(self.formLayoutWidget_5)
        self.bz_BZ_TYPE.setObjectName(u"bz_BZ_TYPE")

        self.formLayout_5.setWidget(2, QFormLayout.FieldRole, self.bz_BZ_TYPE)

        self.label_29 = QLabel(self.formLayoutWidget_5)
        self.label_29.setObjectName(u"label_29")

        self.formLayout_5.setWidget(3, QFormLayout.LabelRole, self.label_29)

        self.bz_BZ_METHOD = QLineEdit(self.formLayoutWidget_5)
        self.bz_BZ_METHOD.setObjectName(u"bz_BZ_METHOD")

        self.formLayout_5.setWidget(3, QFormLayout.FieldRole, self.bz_BZ_METHOD)

        self.label_30 = QLabel(self.formLayoutWidget_5)
        self.label_30.setObjectName(u"label_30")

        self.formLayout_5.setWidget(5, QFormLayout.LabelRole, self.label_30)

        self.bz_USE_YN = QComboBox(self.formLayoutWidget_5)
        self.bz_USE_YN.setObjectName(u"bz_USE_YN")

        self.formLayout_5.setWidget(5, QFormLayout.FieldRole, self.bz_USE_YN)

        self.label_31 = QLabel(self.formLayoutWidget_5)
        self.label_31.setObjectName(u"label_31")

        self.formLayout_5.setWidget(6, QFormLayout.LabelRole, self.label_31)

        self.bz_BZ_DESC = QTextEdit(self.formLayoutWidget_5)
        self.bz_BZ_DESC.setObjectName(u"bz_BZ_DESC")

        self.formLayout_5.setWidget(6, QFormLayout.FieldRole, self.bz_BZ_DESC)

        self.label_28 = QLabel(self.formLayoutWidget_5)
        self.label_28.setObjectName(u"label_28")

        self.formLayout_5.setWidget(4, QFormLayout.LabelRole, self.label_28)

        self.bz_SEC = QLineEdit(self.formLayoutWidget_5)
        self.bz_SEC.setObjectName(u"bz_SEC")

        self.formLayout_5.setWidget(4, QFormLayout.FieldRole, self.bz_SEC)

        self.layoutWidget_3 = QWidget(self.tab_4)
        self.layoutWidget_3.setObjectName(u"layoutWidget_3")
        self.layoutWidget_3.setGeometry(QRect(840, 30, 155, 28))
        self.gridLayout_4 = QGridLayout(self.layoutWidget_3)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.btn_addBz = QToolButton(self.layoutWidget_3)
        self.btn_addBz.setObjectName(u"btn_addBz")

        self.gridLayout_4.addWidget(self.btn_addBz, 0, 0, 1, 1)

        self.btn_delBz = QToolButton(self.layoutWidget_3)
        self.btn_delBz.setObjectName(u"btn_delBz")

        self.gridLayout_4.addWidget(self.btn_delBz, 0, 2, 1, 1)

        self.btn_saveBz = QToolButton(self.layoutWidget_3)
        self.btn_saveBz.setObjectName(u"btn_saveBz")

        self.gridLayout_4.addWidget(self.btn_saveBz, 0, 1, 1, 1)

        self.layoutWidget_4 = QWidget(self.tab_4)
        self.layoutWidget_4.setObjectName(u"layoutWidget_4")
        self.layoutWidget_4.setGeometry(QRect(840, 280, 155, 28))
        self.gridLayout_5 = QGridLayout(self.layoutWidget_4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.btn_addSch = QToolButton(self.layoutWidget_4)
        self.btn_addSch.setObjectName(u"btn_addSch")

        self.gridLayout_5.addWidget(self.btn_addSch, 0, 0, 1, 1)

        self.btn_delSch = QToolButton(self.layoutWidget_4)
        self.btn_delSch.setObjectName(u"btn_delSch")

        self.gridLayout_5.addWidget(self.btn_delSch, 0, 2, 1, 1)

        self.btn_saveSch = QToolButton(self.layoutWidget_4)
        self.btn_saveSch.setObjectName(u"btn_saveSch")

        self.gridLayout_5.addWidget(self.btn_saveSch, 0, 1, 1, 1)

        self.formLayoutWidget_6 = QWidget(self.tab_4)
        self.formLayoutWidget_6.setObjectName(u"formLayoutWidget_6")
        self.formLayoutWidget_6.setGeometry(QRect(840, 310, 271, 281))
        self.formLayout_6 = QFormLayout(self.formLayoutWidget_6)
        self.formLayout_6.setObjectName(u"formLayout_6")
        self.formLayout_6.setContentsMargins(0, 0, 0, 0)
        self.label_32 = QLabel(self.formLayoutWidget_6)
        self.label_32.setObjectName(u"label_32")

        self.formLayout_6.setWidget(0, QFormLayout.LabelRole, self.label_32)

        self.sch_PKG_ID = QLineEdit(self.formLayoutWidget_6)
        self.sch_PKG_ID.setObjectName(u"sch_PKG_ID")

        self.formLayout_6.setWidget(0, QFormLayout.FieldRole, self.sch_PKG_ID)

        self.label_33 = QLabel(self.formLayoutWidget_6)
        self.label_33.setObjectName(u"label_33")

        self.formLayout_6.setWidget(1, QFormLayout.LabelRole, self.label_33)

        self.sch_SCH_ID = QLineEdit(self.formLayoutWidget_6)
        self.sch_SCH_ID.setObjectName(u"sch_SCH_ID")

        self.formLayout_6.setWidget(1, QFormLayout.FieldRole, self.sch_SCH_ID)

        self.label_34 = QLabel(self.formLayoutWidget_6)
        self.label_34.setObjectName(u"label_34")

        self.formLayout_6.setWidget(3, QFormLayout.LabelRole, self.label_34)

        self.sch_SCH_JOB = QLineEdit(self.formLayoutWidget_6)
        self.sch_SCH_JOB.setObjectName(u"sch_SCH_JOB")

        self.formLayout_6.setWidget(3, QFormLayout.FieldRole, self.sch_SCH_JOB)

        self.label_35 = QLabel(self.formLayoutWidget_6)
        self.label_35.setObjectName(u"label_35")

        self.formLayout_6.setWidget(4, QFormLayout.LabelRole, self.label_35)

        self.sch_BZ_METHOD = QLineEdit(self.formLayoutWidget_6)
        self.sch_BZ_METHOD.setObjectName(u"sch_BZ_METHOD")

        self.formLayout_6.setWidget(4, QFormLayout.FieldRole, self.sch_BZ_METHOD)

        self.label_36 = QLabel(self.formLayoutWidget_6)
        self.label_36.setObjectName(u"label_36")

        self.formLayout_6.setWidget(5, QFormLayout.LabelRole, self.label_36)

        self.sch_USE_YN = QComboBox(self.formLayoutWidget_6)
        self.sch_USE_YN.setObjectName(u"sch_USE_YN")

        self.formLayout_6.setWidget(5, QFormLayout.FieldRole, self.sch_USE_YN)

        self.label_37 = QLabel(self.formLayoutWidget_6)
        self.label_37.setObjectName(u"label_37")

        self.formLayout_6.setWidget(6, QFormLayout.LabelRole, self.label_37)

        self.sch_SCH_DESC = QTextEdit(self.formLayoutWidget_6)
        self.sch_SCH_DESC.setObjectName(u"sch_SCH_DESC")

        self.formLayout_6.setWidget(6, QFormLayout.FieldRole, self.sch_SCH_DESC)

        self.ss_3 = QLabel(self.formLayoutWidget_6)
        self.ss_3.setObjectName(u"ss_3")

        self.formLayout_6.setWidget(2, QFormLayout.LabelRole, self.ss_3)

        self.sch_SCH_JOB_TYPE = QComboBox(self.formLayoutWidget_6)
        self.sch_SCH_JOB_TYPE.setObjectName(u"sch_SCH_JOB_TYPE")

        self.formLayout_6.setWidget(2, QFormLayout.FieldRole, self.sch_SCH_JOB_TYPE)

        self.tap_info.addTab(self.tab_4, "")

        self.gridLayout_2.addWidget(self.tap_info, 2, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1150, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tap_info.setCurrentIndex(3)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.btn_addSk.setText(QCoreApplication.translate("MainWindow", u"\uc2e0\uaddc", None))
        self.btn_delSk.setText(QCoreApplication.translate("MainWindow", u"\uc0ad\uc81c", None))
        self.btn_saveSk.setText(QCoreApplication.translate("MainWindow", u"\uc800\uc7a5", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\ud328\ud0a4\uc9c0 \uba85", None))
        self.sk_PKG_ID.setText("")
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"\uc18c\ucf13 \uc544\uc774\ub514", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"\uc18c\ucf13 group", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"desc", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"\ub85c\uadf8 \ucd9c\ub825", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"\uc0ac\uc6a9\uc5ec\ubd80", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"\uc18c\ucf13 \ud0c0\uc785", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"\ub51c\ub9ac\ubbf8\ud130", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"\ud3ec\ud2b8", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"\uc544\uc774\ud53c", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"\ud574\ub354", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"\uc5f0\uacb0\uc720\ud615", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"\uc5f0\uacb0\uc885\ub958", None))
        ___qtablewidgetitem = self.list_sk.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"\uc0c8 \ud589", None));
        self.tap_info.setTabText(self.tap_info.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"\uc18c\ucf13 \ub9ac\uc2a4\ud2b8", None))
        ___qtablewidgetitem1 = self.list_in.horizontalHeaderItem(0)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"\uc0c8 \ud589", None));
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"\ud328\ud0a4\uc9c0 \uba85", None))
        self.in_PKG_ID.setText("")
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"\uc18c\ucf13 \uc544\uc774\ub514", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"\uba54\uc2dc\uc9c0 \uc544\uc774\ub514", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"\ucc98\ub9ac \ud578\ub4e4\ub7ec", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"\uc0ac\uc6a9\uc5ec\ubd80", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"desc", None))
        self.ss.setText(QCoreApplication.translate("MainWindow", u"SEQ", None))
        self.btn_addIn.setText(QCoreApplication.translate("MainWindow", u"\uc2e0\uaddc", None))
        self.btn_delIn.setText(QCoreApplication.translate("MainWindow", u"\uc0ad\uc81c", None))
        self.btn_saveIn.setText(QCoreApplication.translate("MainWindow", u"\uc800\uc7a5", None))
        self.tap_info.setTabText(self.tap_info.indexOf(self.tab_5), QCoreApplication.translate("MainWindow", u"IN \ud328\ud0b7 \uc124\uc815", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\uba54\uc2dc\uc9c0 ID", None))
        self.msg_search.setText(QCoreApplication.translate("MainWindow", u"\uac80\uc0c9", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"MID", None))
        self.msg_add.setText(QCoreApplication.translate("MainWindow", u"\ucd94\uac00", None))
        self.msg_dt_add.setText(QCoreApplication.translate("MainWindow", u"\ucd94\uac00", None))
        self.msg_dt_del.setText(QCoreApplication.translate("MainWindow", u"\uc0ad\uc81c", None))
        self.msg_del.setText(QCoreApplication.translate("MainWindow", u"\uc0ad\uc81c", None))
        self.msg_save.setText(QCoreApplication.translate("MainWindow", u"\uc800\uc7a5", None))
        self.msg_dt_save.setText(QCoreApplication.translate("MainWindow", u"\uc800\uc7a5", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"MSG ID :", None))
        self.selected_msg.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.tap_info.setTabText(self.tap_info.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"\uba54\uc2dc\uc9c0", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\uc774\ubca4\ud2b8 \uc18c\ucf13 \uadf8\ub8f9", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\uc2dc\uc2a4\ud15c SCH \uc2a4\ucf00\uc904", None))
        ___qtablewidgetitem2 = self.list_bz.horizontalHeaderItem(0)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"\uc0c8 \ud589", None));
        ___qtablewidgetitem3 = self.list_sch.horizontalHeaderItem(0)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"\uc0c8 \ud589", None));
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"\ud328\ud0a4\uc9c0 \uba85", None))
        self.bz_PKG_ID.setText("")
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"\uc18c\ucf13 GROUP", None))
        self.ss_2.setText(QCoreApplication.translate("MainWindow", u"\uc774\ubca4\ud2b8 \ud0c0\uc785", None))
        self.label_29.setText(QCoreApplication.translate("MainWindow", u"\ucc98\ub9ac \ud578\ub4e4\ub7ec", None))
        self.label_30.setText(QCoreApplication.translate("MainWindow", u"\uc0ac\uc6a9\uc5ec\ubd80", None))
        self.label_31.setText(QCoreApplication.translate("MainWindow", u"desc", None))
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"\ucd08", None))
        self.btn_addBz.setText(QCoreApplication.translate("MainWindow", u"\uc2e0\uaddc", None))
        self.btn_delBz.setText(QCoreApplication.translate("MainWindow", u"\uc0ad\uc81c", None))
        self.btn_saveBz.setText(QCoreApplication.translate("MainWindow", u"\uc800\uc7a5", None))
        self.btn_addSch.setText(QCoreApplication.translate("MainWindow", u"\uc2e0\uaddc", None))
        self.btn_delSch.setText(QCoreApplication.translate("MainWindow", u"\uc0ad\uc81c", None))
        self.btn_saveSch.setText(QCoreApplication.translate("MainWindow", u"\uc800\uc7a5", None))
        self.label_32.setText(QCoreApplication.translate("MainWindow", u"\ud328\ud0a4\uc9c0 \uba85", None))
        self.sch_PKG_ID.setText("")
        self.label_33.setText(QCoreApplication.translate("MainWindow", u"\uc2a4\ucf00\uc904 ID", None))
        self.label_34.setText(QCoreApplication.translate("MainWindow", u"JOB", None))
        self.label_35.setText(QCoreApplication.translate("MainWindow", u"\ucc98\ub9ac \ud578\ub4e4\ub7ec", None))
        self.label_36.setText(QCoreApplication.translate("MainWindow", u"\uc0ac\uc6a9\uc5ec\ubd80", None))
        self.label_37.setText(QCoreApplication.translate("MainWindow", u"desc", None))
        self.ss_3.setText(QCoreApplication.translate("MainWindow", u"JOB TYPE", None))
        self.tap_info.setTabText(self.tap_info.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"\uc774\ubca4\ud2b8", None))
    # retranslateUi

