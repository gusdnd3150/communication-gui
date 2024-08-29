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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QGridLayout,
    QHeaderView, QLabel, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QStatusBar, QTableWidget,
    QTableWidgetItem, QToolButton, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1087, 570)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(500, 400))
        MainWindow.setMaximumSize(QSize(16777215, 16777215))
        MainWindow.setBaseSize(QSize(650, 300))
        font = QFont()
        font.setFamilies([u"\ub9d1\uc740 \uace0\ub515"])
        font.setBold(True)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet(u"QMainWindow {\n"
"    background-color: #2E2E2E;\n"
"    color: #FFFFFF;\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout_3, 1, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setStyleSheet(u"QLabel{\n"
"	color:white\n"
"}")

        self.verticalLayout.addWidget(self.label_2)

        self.list_run_server = QTableWidget(self.centralwidget)
        self.list_run_server.setObjectName(u"list_run_server")
        font1 = QFont()
        font1.setPointSize(8)
        font1.setBold(False)
        self.list_run_server.setFont(font1)
        self.list_run_server.setAcceptDrops(False)
        self.list_run_server.setAutoFillBackground(True)
        self.list_run_server.setStyleSheet(u"QTableWidget {\n"
"    background-color: #2E2E2E;\n"
"    color: #FFFFFF;\n"
"    gridline-color: #444444;\n"
"    border: 1px solid #444444;\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"    background-color: #444444;\n"
"    color: #FFFFFF;\n"
"    padding: 4px;\n"
"    border: 1px solid #2E2E2E;\n"
"}\n"
"\n"
"QTableWidget::item {\n"
"    border: none;\n"
"    padding: 4px;\n"
"}\n"
"\n"
"QTableWidget::item:selected {\n"
"    background-color: #555555;\n"
"    color: #FFFFFF;\n"
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
"QScrollBar::add-page:vertical, QSc"
                        "rollBar::sub-page:vertical {\n"
"    background: none;\n"
"}")
        self.list_run_server.setDragEnabled(False)
        self.list_run_server.setDragDropOverwriteMode(False)
        self.list_run_server.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.list_run_server.setShowGrid(True)
        self.list_run_server.setSortingEnabled(True)
        self.list_run_server.verticalHeader().setDefaultSectionSize(41)

        self.verticalLayout.addWidget(self.list_run_server)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setStyleSheet(u"QLabel{\n"
"	color:white\n"
"}")

        self.verticalLayout.addWidget(self.label_3)

        self.list_run_client = QTableWidget(self.centralwidget)
        self.list_run_client.setObjectName(u"list_run_client")
        font2 = QFont()
        font2.setPointSize(8)
        self.list_run_client.setFont(font2)
        self.list_run_client.setStyleSheet(u"QTableWidget {\n"
"    background-color: #2E2E2E;\n"
"    color: #FFFFFF;\n"
"    gridline-color: #444444;\n"
"    border: 1px solid #444444;\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"    background-color: #444444;\n"
"    color: #FFFFFF;\n"
"    padding: 4px;\n"
"    border: 1px solid #2E2E2E;\n"
"}\n"
"\n"
"QTableWidget::item {\n"
"    border: none;\n"
"    padding: 4px;\n"
"}\n"
"\n"
"QTableWidget::item:selected {\n"
"    background-color: #555555;\n"
"    color: #FFFFFF;\n"
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
"QScrollBar::add-page:vertical, QSc"
                        "rollBar::sub-page:vertical {\n"
"    background: none;\n"
"}")
        self.list_run_client.setTabKeyNavigation(False)
        self.list_run_client.setProperty("showDropIndicator", False)
        self.list_run_client.setDragDropOverwriteMode(False)
        self.list_run_client.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.verticalLayout.addWidget(self.list_run_client)


        self.gridLayout_2.addLayout(self.verticalLayout, 2, 0, 1, 1)

        self.list_conn = QTableWidget(self.centralwidget)
        self.list_conn.setObjectName(u"list_conn")
        self.list_conn.setMaximumSize(QSize(300, 16777215))
        self.list_conn.setStyleSheet(u"QTableWidget {\n"
"    background-color: #2E2E2E;\n"
"    color: #FFFFFF;\n"
"    gridline-color: #444444;\n"
"    border: 1px solid #444444;\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"    background-color: #444444;\n"
"    color: #FFFFFF;\n"
"    padding: 4px;\n"
"    border: 1px solid #2E2E2E;\n"
"}\n"
"\n"
"QTableWidget::item {\n"
"    border: none;\n"
"    padding: 4px;\n"
"}\n"
"\n"
"QTableWidget::item:selected {\n"
"    background-color: #555555;\n"
"    color: #FFFFFF;\n"
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
"QScrollBar::add-page:vertical, QSc"
                        "rollBar::sub-page:vertical {\n"
"    background: none;\n"
"}")

        self.gridLayout_2.addWidget(self.list_conn, 2, 1, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.btn_settings = QToolButton(self.centralwidget)
        self.btn_settings.setObjectName(u"btn_settings")
        font3 = QFont()
        font3.setFamilies([u"\ub9d1\uc740 \uace0\ub515"])
        self.btn_settings.setFont(font3)
        self.btn_settings.setStyleSheet(u"QToolButton {\n"
"    background-color: #444444;\n"
"    color: #FFFFFF;\n"
"    border: 1px solid #555555;\n"
"    padding: 5px 10px;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QToolButton:hover {\n"
"    background-color: #555555;\n"
"    border: 1px solid #666666;\n"
"}\n"
"\n"
"QToolButton:pressed {\n"
"    background-color: #333333;\n"
"    border: 1px solid #444444;\n"
"}")

        self.gridLayout.addWidget(self.btn_settings, 0, 3, 1, 1)

        self.btn_start = QPushButton(self.centralwidget)
        self.btn_start.setObjectName(u"btn_start")
        self.btn_start.setMaximumSize(QSize(200, 16777215))
        self.btn_start.setFont(font)
        self.btn_start.setStyleSheet(u"QPushButton {\n"
"    background-color: rgb(11, 230, 0);\n"
"    color: black;\n"
"    border: 1px solid #555555;\n"
"    padding: 5px 10px;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(80, 190, 11);\n"
"    border: 1px solid #666666;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(7, 143, 0);\n"
"    border: 1px solid #444444;\n"
"}")

        self.gridLayout.addWidget(self.btn_start, 0, 1, 1, 1)

        self.combo_pkg = QComboBox(self.centralwidget)
        self.combo_pkg.setObjectName(u"combo_pkg")
        self.combo_pkg.setMaximumSize(QSize(200, 16777215))
        self.combo_pkg.setFont(font3)
        self.combo_pkg.setAcceptDrops(False)
        self.combo_pkg.setStyleSheet(u"QComboBox {\n"
"    background-color: #444444;\n"
"    color: #FFFFFF;\n"
"    border: 1px solid #555555;\n"
"    padding: 5px;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    border: 1px solid #666666;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 20px;\n"
"    border-left-width: 1px;\n"
"    border-left-color: #555555;\n"
"    border-left-style: solid;\n"
"    border-top-right-radius: 5px;\n"
"    border-bottom-right-radius: 5px;\n"
"    background-color: #555555;\n"
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

        self.btn_stop = QPushButton(self.centralwidget)
        self.btn_stop.setObjectName(u"btn_stop")
        self.btn_stop.setMaximumSize(QSize(200, 16777215))
        self.btn_stop.setStyleSheet(u"QPushButton {\n"
"    background-color: rgb(180, 74, 3);\n"
"    color: white;\n"
"    border: 1px solid #555555;\n"
"    padding: 5px 10px;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(255, 74, 74);\n"
"    border: 1px solid #666666;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(255, 74, 74);\n"
"    border: 1px solid #444444;\n"
"}")

        self.gridLayout.addWidget(self.btn_stop, 0, 2, 1, 1)

        self.btn_handler = QToolButton(self.centralwidget)
        self.btn_handler.setObjectName(u"btn_handler")
        self.btn_handler.setStyleSheet(u"QToolButton {\n"
"    background-color: #444444;\n"
"    color: #FFFFFF;\n"
"    border: 1px solid #555555;\n"
"    padding: 5px 10px;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QToolButton:hover {\n"
"    background-color: #555555;\n"
"    border: 1px solid #666666;\n"
"}\n"
"\n"
"QToolButton:pressed {\n"
"    background-color: #333333;\n"
"    border: 1px solid #444444;\n"
"}")

        self.gridLayout.addWidget(self.btn_handler, 0, 4, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 2)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setStyleSheet(u"QLabel{\n"
"	color:white\n"
"}")

        self.gridLayout_2.addWidget(self.label_4, 1, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1087, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"--", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"[ Server ]", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"[ Client ]", None))
        self.btn_settings.setText(QCoreApplication.translate("MainWindow", u"settings", None))
        self.btn_start.setText(QCoreApplication.translate("MainWindow", u"Run Application", None))
        self.btn_stop.setText(QCoreApplication.translate("MainWindow", u"Stop Application", None))
        self.btn_handler.setText(QCoreApplication.translate("MainWindow", u"Handler", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Connection List", None))
    # retranslateUi

