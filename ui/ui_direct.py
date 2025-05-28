# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sk_direct.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QGridLayout,
    QHBoxLayout, QLabel, QMainWindow, QMenuBar,
    QPlainTextEdit, QPushButton, QSizePolicy, QStatusBar,
    QVBoxLayout, QWidget)

class Ui_Direct(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(333, 426)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.dir_input = QPlainTextEdit(self.centralwidget)
        self.dir_input.setObjectName(u"dir_input")

        self.verticalLayout.addWidget(self.dir_input)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.dir_string = QPushButton(self.centralwidget)
        self.dir_string.setObjectName(u"dir_string")

        self.verticalLayout_2.addWidget(self.dir_string)

        self.dir_float = QPushButton(self.centralwidget)
        self.dir_float.setObjectName(u"dir_float")

        self.verticalLayout_2.addWidget(self.dir_float)

        self.dir_int = QPushButton(self.centralwidget)
        self.dir_int.setObjectName(u"dir_int")

        self.verticalLayout_2.addWidget(self.dir_int)

        self.dir_double = QPushButton(self.centralwidget)
        self.dir_double.setObjectName(u"dir_double")

        self.verticalLayout_2.addWidget(self.dir_double)

        self.dir_decimal = QPushButton(self.centralwidget)
        self.dir_decimal.setObjectName(u"dir_decimal")

        self.verticalLayout_2.addWidget(self.dir_decimal)

        self.dir_decimals = QPushButton(self.centralwidget)
        self.dir_decimals.setObjectName(u"dir_decimals")

        self.verticalLayout_2.addWidget(self.dir_decimals)


        self.horizontalLayout.addLayout(self.verticalLayout_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_6.addWidget(self.label_5)

        self.dir_buffer = QPlainTextEdit(self.centralwidget)
        self.dir_buffer.setObjectName(u"dir_buffer")

        self.verticalLayout_6.addWidget(self.dir_buffer)

        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.dir_send = QPushButton(self.centralwidget)
        self.dir_send.setObjectName(u"dir_send")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.dir_send)

        self.dir_sk = QComboBox(self.centralwidget)
        self.dir_sk.setObjectName(u"dir_sk")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.dir_sk)


        self.verticalLayout_6.addLayout(self.formLayout_2)


        self.verticalLayout_3.addLayout(self.verticalLayout_6)


        self.verticalLayout_4.addLayout(self.verticalLayout_3)


        self.horizontalLayout_2.addLayout(self.verticalLayout_4)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")

        self.horizontalLayout_2.addLayout(self.verticalLayout_5)


        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 333, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Input", None))
        self.dir_string.setText(QCoreApplication.translate("MainWindow", u"String", None))
        self.dir_float.setText(QCoreApplication.translate("MainWindow", u"float", None))
        self.dir_int.setText(QCoreApplication.translate("MainWindow", u"int", None))
        self.dir_double.setText(QCoreApplication.translate("MainWindow", u"Double", None))
        self.dir_decimal.setText(QCoreApplication.translate("MainWindow", u"decimal", None))
        self.dir_decimals.setText(QCoreApplication.translate("MainWindow", u"decimal arr", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Buffer", None))
        self.dir_send.setText(QCoreApplication.translate("MainWindow", u"Send", None))
    # retranslateUi

