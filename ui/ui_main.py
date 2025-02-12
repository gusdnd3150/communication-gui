# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QComboBox,
    QFrame, QGridLayout, QHeaderView, QMainWindow,
    QMenu, QMenuBar, QPushButton, QScrollArea,
    QSizePolicy, QStatusBar, QTabWidget, QTableWidget,
    QTableWidgetItem, QTextEdit, QTreeView, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(687, 512)
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
        self.action_settings = QAction(MainWindow)
        self.action_settings.setObjectName(u"action_settings")
        self.actionOpen_log_folder = QAction(MainWindow)
        self.actionOpen_log_folder.setObjectName(u"actionOpen_log_folder")
        self.action_test = QAction(MainWindow)
        self.action_test.setObjectName(u"action_test")
        self.action_util = QAction(MainWindow)
        self.action_util.setObjectName(u"action_util")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_3 = QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(False)
        self.tabWidget.setFont(font1)
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.gridLayout_5 = QGridLayout(self.tab_2)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.list_run_server = QTableWidget(self.tab_2)
        self.list_run_server.setObjectName(u"list_run_server")
        self.list_run_server.setMaximumSize(QSize(16777215, 16777215))
        font2 = QFont()
        font2.setFamilies([u"\ub9d1\uc740 \uace0\ub515"])
        font2.setPointSize(9)
        font2.setBold(False)
        font2.setItalic(False)
        self.list_run_server.setFont(font2)
        self.list_run_server.setAcceptDrops(False)
        self.list_run_server.setAutoFillBackground(True)
        self.list_run_server.setStyleSheet(u"font: 9pt \"\ub9d1\uc740 \uace0\ub515\";")
        self.list_run_server.setDragEnabled(False)
        self.list_run_server.setDragDropOverwriteMode(False)
        self.list_run_server.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.list_run_server.setShowGrid(True)
        self.list_run_server.setSortingEnabled(False)
        self.list_run_server.horizontalHeader().setProperty(u"showSortIndicator", False)
        self.list_run_server.verticalHeader().setDefaultSectionSize(30)

        self.gridLayout_5.addWidget(self.list_run_server, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.gridLayout_6 = QGridLayout(self.tab_3)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.list_run_client = QTableWidget(self.tab_3)
        self.list_run_client.setObjectName(u"list_run_client")
        self.list_run_client.setMaximumSize(QSize(16777215, 16777215))
        self.list_run_client.setFont(font2)
        self.list_run_client.setAutoFillBackground(True)
        self.list_run_client.setStyleSheet(u"font: 9pt \"\ub9d1\uc740 \uace0\ub515\";")
        self.list_run_client.setTabKeyNavigation(True)
        self.list_run_client.setProperty(u"showDropIndicator", True)
        self.list_run_client.setDragDropOverwriteMode(False)
        self.list_run_client.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.gridLayout_6.addWidget(self.list_run_client, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.gridLayout_7 = QGridLayout(self.tab_4)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.list_conn = QTreeView(self.tab_4)
        self.list_conn.setObjectName(u"list_conn")
        self.list_conn.setEnabled(True)
        self.list_conn.setMaximumSize(QSize(16777215, 16777215))
        font3 = QFont()
        font3.setPointSize(8)
        self.list_conn.setFont(font3)
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

        self.gridLayout_7.addWidget(self.list_conn, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_4, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout_4 = QGridLayout(self.tab)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.log_chk_showlog = QCheckBox(self.tab)
        self.log_chk_showlog.setObjectName(u"log_chk_showlog")

        self.gridLayout_4.addWidget(self.log_chk_showlog, 0, 0, 1, 1)

        self.log_text_log = QTextEdit(self.tab)
        self.log_text_log.setObjectName(u"log_text_log")
        self.log_text_log.setLineWrapMode(QTextEdit.NoWrap)
        self.log_text_log.setReadOnly(True)
        self.log_text_log.setAcceptRichText(True)

        self.gridLayout_4.addWidget(self.log_text_log, 3, 0, 1, 1)

        self.log_btn_clear = QPushButton(self.tab)
        self.log_btn_clear.setObjectName(u"log_btn_clear")

        self.gridLayout_4.addWidget(self.log_btn_clear, 1, 0, 1, 1)

        self.tabWidget.addTab(self.tab, "")

        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 1, 1, 1)

        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy1)
        self.scrollArea.setMinimumSize(QSize(75, 0))
        self.scrollArea.setFrameShadow(QFrame.Raised)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 73, 449))
        self.btn_stop = QPushButton(self.scrollAreaWidgetContents)
        self.btn_stop.setObjectName(u"btn_stop")
        self.btn_stop.setGeometry(QRect(0, 70, 71, 22))
        self.btn_stop.setMaximumSize(QSize(200, 16777215))
        font4 = QFont()
        font4.setFamilies([u"\ub9d1\uc740 \uace0\ub515"])
        font4.setPointSize(10)
        font4.setBold(True)
        font4.setUnderline(False)
        font4.setStrikeOut(False)
        self.btn_stop.setFont(font4)
        self.btn_stop.setStyleSheet(u"/* \uc77c\ubc18 \ubc84\ud2bc \uc2a4\ud0c0\uc77c */\n"
"QPushButton {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(250, 90, 90, 255), stop:1 rgba(232, 81, 81, 255));\n"
"    border: none;\n"
"    border-radius: 4px;\n"
"    color: white;\n"
"    padding: 2px\n"
"}\n"
"\n"
"/* Hover \uc0c1\ud0dc\uc5d0\uc11c \ubc30\uacbd\uc0c9 \ubcc0\uacbd */\n"
"QPushButton:hover {\n"
"    background-color: #E35252;\n"
"}")
        self.btn_start = QPushButton(self.scrollAreaWidgetContents)
        self.btn_start.setObjectName(u"btn_start")
        self.btn_start.setGeometry(QRect(0, 40, 71, 22))
        self.btn_start.setMaximumSize(QSize(200, 16777215))
        font5 = QFont()
        font5.setFamilies([u"\ub9d1\uc740 \uace0\ub515"])
        font5.setPointSize(10)
        font5.setBold(True)
        self.btn_start.setFont(font5)
        self.btn_start.setStyleSheet(u"QPushButton {\n"
"    background-color: #22e117;\n"
"    border: none;\n"
"    border-radius: 4px;\n"
"    color: white;\n"
"    padding: 2px\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #33c12b;\n"
"}")
        self.combo_pkg = QComboBox(self.scrollAreaWidgetContents)
        self.combo_pkg.setObjectName(u"combo_pkg")
        self.combo_pkg.setGeometry(QRect(0, 10, 71, 24))
        self.combo_pkg.setMaximumSize(QSize(200, 16777215))
        font6 = QFont()
        font6.setFamilies([u"\ub9d1\uc740 \uace0\ub515"])
        font6.setPointSize(10)
        self.combo_pkg.setFont(font6)
        self.combo_pkg.setAcceptDrops(False)
        self.combo_pkg.setStyleSheet(u"")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_3.addWidget(self.scrollArea, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 687, 22))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        self.menu_2 = QMenu(self.menubar)
        self.menu_2.setObjectName(u"menu_2")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menu.addAction(self.action_settings)
        self.menu.addAction(self.action_test)
        self.menu.addAction(self.action_util)
        self.menu_2.addAction(self.actionOpen_log_folder)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.action_settings.setText(QCoreApplication.translate("MainWindow", u"Socket settings", None))
        self.actionOpen_log_folder.setText(QCoreApplication.translate("MainWindow", u"Open log folder", None))
        self.action_test.setText(QCoreApplication.translate("MainWindow", u"Socket Test", None))
        self.action_util.setText(QCoreApplication.translate("MainWindow", u"Utility", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Server", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Client", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"Connection List", None))
        self.log_chk_showlog.setText(QCoreApplication.translate("MainWindow", u"show log", None))
        self.log_text_log.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'\ub9d1\uc740 \uace0\ub515'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Gulim'; font-size:9pt;\"><br /></p></body></html>", None))
        self.log_btn_clear.setText(QCoreApplication.translate("MainWindow", u"clear", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Log", None))
        self.btn_stop.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.btn_start.setText(QCoreApplication.translate("MainWindow", u"run", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\uc124\uc815", None))
        self.menu_2.setTitle(QCoreApplication.translate("MainWindow", u"\ud30c\uc77c", None))
    # retranslateUi

