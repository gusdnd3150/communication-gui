# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'handler.ui'
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
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QTableWidget, QTableWidgetItem, QToolButton,
    QWidget)

class Ui_Handler(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1119, 518)
        MainWindow.setBaseSize(QSize(1000, 0))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_3 = QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.input_handle_search = QLineEdit(self.centralwidget)
        self.input_handle_search.setObjectName(u"input_handle_search")

        self.gridLayout.addWidget(self.input_handle_search, 1, 0, 1, 1)

        self.list_handle_msg = QTableWidget(self.centralwidget)
        self.list_handle_msg.setObjectName(u"list_handle_msg")
        self.list_handle_msg.setSelectionMode(QAbstractItemView.SingleSelection)
        self.list_handle_msg.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.gridLayout.addWidget(self.list_handle_msg, 4, 0, 1, 2)

        self.btn_handle_search = QPushButton(self.centralwidget)
        self.btn_handle_search.setObjectName(u"btn_handle_search")

        self.gridLayout.addWidget(self.btn_handle_search, 1, 1, 1, 1)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)


        self.horizontalLayout.addLayout(self.gridLayout)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.btn_handle_send = QPushButton(self.centralwidget)
        self.btn_handle_send.setObjectName(u"btn_handle_send")

        self.gridLayout_2.addWidget(self.btn_handle_send, 6, 0, 1, 1)

        self.combo_sk_list = QComboBox(self.centralwidget)
        self.combo_sk_list.setObjectName(u"combo_sk_list")

        self.gridLayout_2.addWidget(self.combo_sk_list, 1, 0, 1, 1)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 3, 0, 1, 1)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)

        self.list_handle_body = QTableWidget(self.centralwidget)
        self.list_handle_body.setObjectName(u"list_handle_body")

        self.gridLayout_2.addWidget(self.list_handle_body, 4, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.btn_save_dt_val = QToolButton(self.centralwidget)
        self.btn_save_dt_val.setObjectName(u"btn_save_dt_val")

        self.horizontalLayout_3.addWidget(self.btn_save_dt_val)


        self.gridLayout_2.addLayout(self.horizontalLayout_3, 5, 0, 1, 1)


        self.horizontalLayout.addLayout(self.gridLayout_2)


        self.gridLayout_3.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1119, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.btn_handle_search.setText(QCoreApplication.translate("MainWindow", u"\uac80\uc0c9", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\uba54\uc2dc\uc9c0 \ub9ac\uc2a4\ud2b8", None))
        self.btn_handle_send.setText(QCoreApplication.translate("MainWindow", u"Send", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\uba54\uc2dc\uc9c0 BODY", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\uc18c\ucf13 \uc544\uc774\ub514", None))
        self.btn_save_dt_val.setText(QCoreApplication.translate("MainWindow", u"save Default", None))
    # retranslateUi

