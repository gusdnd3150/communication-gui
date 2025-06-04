# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_new.ui'
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
    QFrame, QGridLayout, QHBoxLayout, QHeaderView,
    QLabel, QLayout, QLineEdit, QMainWindow,
    QMenu, QMenuBar, QPushButton, QScrollArea,
    QSizePolicy, QSplitter, QStatusBar, QTabWidget,
    QTableWidget, QTableWidgetItem, QTextEdit, QToolButton,
    QTreeView, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(931, 711)
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
        self.action_dirMessage = QAction(MainWindow)
        self.action_dirMessage.setObjectName(u"action_dirMessage")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_8 = QGridLayout(self.centralwidget)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
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
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 73, 648))
        self.btn_stop = QPushButton(self.scrollAreaWidgetContents)
        self.btn_stop.setObjectName(u"btn_stop")
        self.btn_stop.setGeometry(QRect(0, 70, 71, 22))
        self.btn_stop.setMaximumSize(QSize(200, 16777215))
        font1 = QFont()
        font1.setFamilies([u"\ub9d1\uc740 \uace0\ub515"])
        font1.setPointSize(10)
        font1.setBold(True)
        font1.setUnderline(False)
        font1.setStrikeOut(False)
        self.btn_stop.setFont(font1)
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
        font2 = QFont()
        font2.setFamilies([u"\ub9d1\uc740 \uace0\ub515"])
        font2.setPointSize(10)
        font2.setBold(True)
        self.btn_start.setFont(font2)
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
        font3 = QFont()
        font3.setFamilies([u"\ub9d1\uc740 \uace0\ub515"])
        font3.setPointSize(10)
        self.combo_pkg.setFont(font3)
        self.combo_pkg.setAcceptDrops(False)
        self.combo_pkg.setStyleSheet(u"")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_8.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        font4 = QFont()
        font4.setPointSize(10)
        font4.setBold(False)
        self.tabWidget.setFont(font4)
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.gridLayout_5 = QGridLayout(self.tab_2)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.list_run_server = QTableWidget(self.tab_2)
        self.list_run_server.setObjectName(u"list_run_server")
        self.list_run_server.setMaximumSize(QSize(16777215, 16777215))
        font5 = QFont()
        font5.setFamilies([u"\ub9d1\uc740 \uace0\ub515"])
        font5.setPointSize(9)
        font5.setBold(False)
        font5.setItalic(False)
        self.list_run_server.setFont(font5)
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
        self.list_run_client.setFont(font5)
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
        font6 = QFont()
        font6.setPointSize(8)
        self.list_conn.setFont(font6)
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
        self.gridLayout = QGridLayout(self.tab)
        self.gridLayout.setObjectName(u"gridLayout")
        self.splitter = QSplitter(self.tab)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.verticalWidget = QWidget(self.splitter)
        self.verticalWidget.setObjectName(u"verticalWidget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.verticalWidget.sizePolicy().hasHeightForWidth())
        self.verticalWidget.setSizePolicy(sizePolicy2)
        self.verticalWidget.setMaximumSize(QSize(9999999, 16777215))
        self.verticalLayout = QVBoxLayout(self.verticalWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.log_chk_showlog = QCheckBox(self.verticalWidget)
        self.log_chk_showlog.setObjectName(u"log_chk_showlog")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.log_chk_showlog.sizePolicy().hasHeightForWidth())
        self.log_chk_showlog.setSizePolicy(sizePolicy3)

        self.verticalLayout.addWidget(self.log_chk_showlog)

        self.log_btn_clear = QPushButton(self.verticalWidget)
        self.log_btn_clear.setObjectName(u"log_btn_clear")
        sizePolicy3.setHeightForWidth(self.log_btn_clear.sizePolicy().hasHeightForWidth())
        self.log_btn_clear.setSizePolicy(sizePolicy3)

        self.verticalLayout.addWidget(self.log_btn_clear)

        self.log_text_log = QTextEdit(self.verticalWidget)
        self.log_text_log.setObjectName(u"log_text_log")
        sizePolicy.setHeightForWidth(self.log_text_log.sizePolicy().hasHeightForWidth())
        self.log_text_log.setSizePolicy(sizePolicy)
        self.log_text_log.setLineWrapMode(QTextEdit.NoWrap)
        self.log_text_log.setReadOnly(True)
        self.log_text_log.setAcceptRichText(True)

        self.verticalLayout.addWidget(self.log_text_log)

        self.splitter.addWidget(self.verticalWidget)
        self.widget = QWidget(self.splitter)
        self.widget.setObjectName(u"widget")
        self.widget.setEnabled(True)
        sizePolicy2.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy2)
        self.widget.setMinimumSize(QSize(314, 0))
        self.widget.setMaximumSize(QSize(500, 16777215))
        self.gridLayout_3 = QGridLayout(self.widget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setSizeConstraint(QLayout.SetNoConstraint)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(1)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setSizeConstraint(QLayout.SetMinimumSize)
        self.main_btn_save_dt_val = QToolButton(self.widget)
        self.main_btn_save_dt_val.setObjectName(u"main_btn_save_dt_val")

        self.horizontalLayout_3.addWidget(self.main_btn_save_dt_val)


        self.gridLayout_3.addLayout(self.horizontalLayout_3, 9, 0, 1, 1)

        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_3.addWidget(self.label_3, 3, 0, 1, 1)

        self.main_combo_sk_list = QComboBox(self.widget)
        self.main_combo_sk_list.setObjectName(u"main_combo_sk_list")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.main_combo_sk_list.sizePolicy().hasHeightForWidth())
        self.main_combo_sk_list.setSizePolicy(sizePolicy4)

        self.gridLayout_3.addWidget(self.main_combo_sk_list, 11, 0, 1, 1)

        self.main_btn_handle_send = QPushButton(self.widget)
        self.main_btn_handle_send.setObjectName(u"main_btn_handle_send")

        self.gridLayout_3.addWidget(self.main_btn_handle_send, 12, 0, 1, 1)

        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")

        self.gridLayout_3.addWidget(self.label, 7, 0, 1, 1)

        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_3.addWidget(self.label_2, 10, 0, 1, 1)

        self.main_btn_handle_search = QPushButton(self.widget)
        self.main_btn_handle_search.setObjectName(u"main_btn_handle_search")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.main_btn_handle_search.sizePolicy().hasHeightForWidth())
        self.main_btn_handle_search.setSizePolicy(sizePolicy5)

        self.gridLayout_3.addWidget(self.main_btn_handle_search, 5, 0, 1, 1)

        self.main_list_handle_msg = QTableWidget(self.widget)
        self.main_list_handle_msg.setObjectName(u"main_list_handle_msg")
        sizePolicy.setHeightForWidth(self.main_list_handle_msg.sizePolicy().hasHeightForWidth())
        self.main_list_handle_msg.setSizePolicy(sizePolicy)
        self.main_list_handle_msg.setSelectionMode(QAbstractItemView.SingleSelection)
        self.main_list_handle_msg.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.gridLayout_3.addWidget(self.main_list_handle_msg, 6, 0, 1, 1)

        self.main_list_handle_body = QTableWidget(self.widget)
        self.main_list_handle_body.setObjectName(u"main_list_handle_body")
        sizePolicy.setHeightForWidth(self.main_list_handle_body.sizePolicy().hasHeightForWidth())
        self.main_list_handle_body.setSizePolicy(sizePolicy)

        self.gridLayout_3.addWidget(self.main_list_handle_body, 8, 0, 1, 1)

        self.main_handle_search = QLineEdit(self.widget)
        self.main_handle_search.setObjectName(u"main_handle_search")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.main_handle_search.sizePolicy().hasHeightForWidth())
        self.main_handle_search.setSizePolicy(sizePolicy6)

        self.gridLayout_3.addWidget(self.main_handle_search, 4, 0, 1, 1)

        self.splitter.addWidget(self.widget)

        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab, "")

        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)


        self.gridLayout_8.addLayout(self.gridLayout_2, 0, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 931, 22))
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
        self.menu.addAction(self.action_dirMessage)
        self.menu.addAction(self.action_util)
        self.menu_2.addAction(self.actionOpen_log_folder)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(3)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.action_settings.setText(QCoreApplication.translate("MainWindow", u"Socket settings", None))
        self.actionOpen_log_folder.setText(QCoreApplication.translate("MainWindow", u"Open log folder", None))
        self.action_test.setText(QCoreApplication.translate("MainWindow", u"Send Message", None))
        self.action_util.setText(QCoreApplication.translate("MainWindow", u"Utility", None))
        self.action_dirMessage.setText(QCoreApplication.translate("MainWindow", u"Send Direct Message", None))
        self.btn_stop.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.btn_start.setText(QCoreApplication.translate("MainWindow", u"run", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Server", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Client", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"Connection List", None))
        self.log_chk_showlog.setText(QCoreApplication.translate("MainWindow", u"show log", None))
        self.log_btn_clear.setText(QCoreApplication.translate("MainWindow", u"clear", None))
        self.log_text_log.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'\ub9d1\uc740 \uace0\ub515'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Gulim'; font-size:9pt;\"><br /></p></body></html>", None))
        self.main_btn_save_dt_val.setText(QCoreApplication.translate("MainWindow", u"save Default", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\uba54\uc2dc\uc9c0 \ub9ac\uc2a4\ud2b8", None))
        self.main_btn_handle_send.setText(QCoreApplication.translate("MainWindow", u"Send", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\uba54\uc2dc\uc9c0 BODY", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\uc18c\ucf13 \uc544\uc774\ub514", None))
        self.main_btn_handle_search.setText(QCoreApplication.translate("MainWindow", u"\uac80\uc0c9", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Log", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\uc124\uc815", None))
        self.menu_2.setTitle(QCoreApplication.translate("MainWindow", u"\ud30c\uc77c", None))
    # retranslateUi

