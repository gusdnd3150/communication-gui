# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QFrame,
    QGridLayout, QHBoxLayout, QHeaderView, QLabel,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QTabWidget, QTableWidget, QTableWidgetItem,
    QToolButton, QTreeView, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(556, 660)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(400, 400))
        MainWindow.setMaximumSize(QSize(16777215, 16777215))
        MainWindow.setBaseSize(QSize(499, 300))
        font = QFont()
        font.setFamilies([u"\ub9d1\uc740 \uace0\ub515"])
        font.setBold(True)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet(u"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.btn_settings = QToolButton(self.centralwidget)
        self.btn_settings.setObjectName(u"btn_settings")
        font1 = QFont()
        font1.setFamilies([u"\ub9d1\uc740 \uace0\ub515"])
        self.btn_settings.setFont(font1)
        self.btn_settings.setStyleSheet(u"QPushButton {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(27, 188, 194, 255), stop:1 rgba(24, 163, 168, 255));\n"
"    border: none;\n"
"    border-radius: 4px;\n"
"    color: white;\n"
"    padding: 5px\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #169499;\n"
"}")

        self.gridLayout.addWidget(self.btn_settings, 0, 3, 1, 1)

        self.combo_pkg = QComboBox(self.centralwidget)
        self.combo_pkg.setObjectName(u"combo_pkg")
        self.combo_pkg.setMaximumSize(QSize(200, 16777215))
        self.combo_pkg.setFont(font1)
        self.combo_pkg.setAcceptDrops(False)
        self.combo_pkg.setStyleSheet(u"QComboBox {\n"
"    border: 1px solid #555555;\n"
"    padding: 5px;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    border: 1px solid #666666;\n"
"}\n"
"\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #444444;\n"
"    color: #FFFFFF;\n"
"    selection-background-color: #555555;\n"
"    selection-color: #FFFFFF;\n"
"}")

        self.gridLayout.addWidget(self.combo_pkg, 0, 0, 1, 1)

        self.btn_handler = QToolButton(self.centralwidget)
        self.btn_handler.setObjectName(u"btn_handler")
        self.btn_handler.setStyleSheet(u"QPushButton {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(27, 188, 194, 255), stop:1 rgba(24, 163, 168, 255));\n"
"    border: none;\n"
"    border-radius: 4px;\n"
"    color: white;\n"
"    padding: 5px\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #169499;\n"
"}")

        self.gridLayout.addWidget(self.btn_handler, 0, 4, 1, 1)

        self.btn_start = QPushButton(self.centralwidget)
        self.btn_start.setObjectName(u"btn_start")
        self.btn_start.setMaximumSize(QSize(200, 16777215))
        self.btn_start.setFont(font)
        self.btn_start.setStyleSheet(u"QPushButton {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(27, 188, 194, 255), stop:1 rgba(24, 163, 168, 255));\n"
"    border: none;\n"
"    border-radius: 4px;\n"
"    color: white;\n"
"    padding: 5px\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #169499;\n"
"}")

        self.gridLayout.addWidget(self.btn_start, 0, 1, 1, 1)

        self.btn_stop = QPushButton(self.centralwidget)
        self.btn_stop.setObjectName(u"btn_stop")
        self.btn_stop.setMaximumSize(QSize(200, 16777215))
        font2 = QFont()
        font2.setFamilies([u"\ub9d1\uc740 \uace0\ub515"])
        font2.setBold(True)
        font2.setUnderline(False)
        font2.setStrikeOut(False)
        self.btn_stop.setFont(font2)
        self.btn_stop.setStyleSheet(u"/* \uc77c\ubc18 \ubc84\ud2bc \uc2a4\ud0c0\uc77c */\n"
"QPushButton {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(250, 90, 90, 255), stop:1 rgba(232, 81, 81, 255));\n"
"    border: none;\n"
"    border-radius: 4px;\n"
"    color: white;\n"
"    padding: 5px\n"
"}\n"
"\n"
"/* Hover \uc0c1\ud0dc\uc5d0\uc11c \ubc30\uacbd\uc0c9 \ubcc0\uacbd */\n"
"QPushButton:hover {\n"
"    background-color: #E35252;\n"
"}")

        self.gridLayout.addWidget(self.btn_stop, 0, 2, 1, 1)

        self.btn_show_log = QToolButton(self.centralwidget)
        self.btn_show_log.setObjectName(u"btn_show_log")
        self.btn_show_log.setStyleSheet(u"QPushButton {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(27, 188, 194, 255), stop:1 rgba(24, 163, 168, 255));\n"
"    border: none;\n"
"    border-radius: 4px;\n"
"    color: white;\n"
"    padding: 5px\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #169499;\n"
"}")

        self.gridLayout.addWidget(self.btn_show_log, 0, 5, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")

        self.gridLayout_2.addLayout(self.gridLayout_3, 1, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setStyleSheet(u"")

        self.verticalLayout.addWidget(self.label_2)

        self.list_run_server = QTableWidget(self.centralwidget)
        self.list_run_server.setObjectName(u"list_run_server")
        self.list_run_server.setMaximumSize(QSize(16777215, 200))
        font3 = QFont()
        font3.setFamilies([u"\ub9d1\uc740 \uace0\ub515"])
        font3.setPointSize(9)
        font3.setBold(False)
        font3.setItalic(False)
        self.list_run_server.setFont(font3)
        self.list_run_server.setAcceptDrops(False)
        self.list_run_server.setAutoFillBackground(True)
        self.list_run_server.setStyleSheet(u"font: 9pt \"\ub9d1\uc740 \uace0\ub515\";")
        self.list_run_server.setDragEnabled(False)
        self.list_run_server.setDragDropOverwriteMode(False)
        self.list_run_server.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.list_run_server.setShowGrid(True)
        self.list_run_server.setSortingEnabled(False)
        self.list_run_server.horizontalHeader().setProperty("showSortIndicator", False)
        self.list_run_server.verticalHeader().setDefaultSectionSize(30)

        self.verticalLayout.addWidget(self.list_run_server)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setStyleSheet(u"")

        self.verticalLayout.addWidget(self.label_3)

        self.list_run_client = QTableWidget(self.centralwidget)
        self.list_run_client.setObjectName(u"list_run_client")
        self.list_run_client.setMaximumSize(QSize(16777215, 200))
        self.list_run_client.setFont(font3)
        self.list_run_client.setAutoFillBackground(True)
        self.list_run_client.setStyleSheet(u"font: 9pt \"\ub9d1\uc740 \uace0\ub515\";")
        self.list_run_client.setTabKeyNavigation(True)
        self.list_run_client.setProperty("showDropIndicator", True)
        self.list_run_client.setDragDropOverwriteMode(False)
        self.list_run_client.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.verticalLayout.addWidget(self.list_run_client)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.ddddd = QTabWidget(self.centralwidget)
        self.ddddd.setObjectName(u"ddddd")
        self.ddddd.setStyleSheet(u"")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout_4 = QGridLayout(self.tab)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.list_conn = QTreeView(self.tab)
        self.list_conn.setObjectName(u"list_conn")
        self.list_conn.setEnabled(True)
        self.list_conn.setMaximumSize(QSize(16777215, 16777215))
        self.list_conn.setStyleSheet(u"QTreeView{\n"
"	background-color: white;\n"
"	color:black\n"
"}\n"
"\n"
"QScrollBar:vertical {\n"
"    background-color: #2E2E2E;\n"
"    width: 3px;\n"
"	height:2px;\n"
"    margin: 15px 0 15px 0;\n"
"}\n"
"QScrollBar::handle:vertical {\n"
"    background-color: #555555;\n"
"    min-height: 5px;\n"
"}\n"
"QScrollBar:horizontal {\n"
"    background-color: #2E2E2E;\n"
"    height: 8px; \n"
"    margin: 0 15px 0 15px;\n"
"}\n"
"\n"
"QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {\n"
"    background-color: #444444;\n"
"    height: 5px;\n"
"}\n"
"\n"
"QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"    background: none;\n"
"}")
        self.list_conn.setFrameShadow(QFrame.Sunken)
        self.list_conn.setLineWidth(200)
        self.list_conn.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.gridLayout_4.addWidget(self.list_conn, 0, 0, 1, 1)

        self.ddddd.addTab(self.tab, "")

        self.verticalLayout.addWidget(self.ddddd)


        self.gridLayout_2.addLayout(self.verticalLayout, 2, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 556, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.ddddd.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.btn_settings.setText(QCoreApplication.translate("MainWindow", u"settings", None))
        self.btn_handler.setText(QCoreApplication.translate("MainWindow", u"handler", None))
        self.btn_start.setText(QCoreApplication.translate("MainWindow", u"run", None))
        self.btn_stop.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.btn_show_log.setText(QCoreApplication.translate("MainWindow", u"log", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"[ Server ]", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"[ Client ]", None))
        self.ddddd.setTabText(self.ddddd.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Connection List", None))
    # retranslateUi

