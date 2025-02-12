# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'utilty.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QMainWindow,
    QMenuBar, QPushButton, QScrollArea, QSizePolicy,
    QStatusBar, QTabWidget, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(756, 639)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout = QGridLayout(self.tab)
        self.gridLayout.setObjectName(u"gridLayout")
        self.util_encode = QTextEdit(self.tab)
        self.util_encode.setObjectName(u"util_encode")

        self.gridLayout.addWidget(self.util_encode, 0, 2, 2, 1)

        self.util_text = QTextEdit(self.tab)
        self.util_text.setObjectName(u"util_text")

        self.gridLayout.addWidget(self.util_text, 1, 0, 1, 1)

        self.util_combo = QComboBox(self.tab)
        self.util_combo.setObjectName(u"util_combo")

        self.gridLayout.addWidget(self.util_combo, 0, 0, 1, 1)

        self.scrollArea = QScrollArea(self.tab)
        self.scrollArea.setObjectName(u"scrollArea")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 93, 533))
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.btn_util_hex = QPushButton(self.scrollAreaWidgetContents)
        self.btn_util_hex.setObjectName(u"btn_util_hex")

        self.verticalLayout.addWidget(self.btn_util_hex)

        self.btn_util_decimal = QPushButton(self.scrollAreaWidgetContents)
        self.btn_util_decimal.setObjectName(u"btn_util_decimal")

        self.verticalLayout.addWidget(self.btn_util_decimal)

        self.btn_util_binuary = QPushButton(self.scrollAreaWidgetContents)
        self.btn_util_binuary.setObjectName(u"btn_util_binuary")

        self.verticalLayout.addWidget(self.btn_util_binuary)

        self.btn_util_base64 = QPushButton(self.scrollAreaWidgetContents)
        self.btn_util_base64.setObjectName(u"btn_util_base64")

        self.verticalLayout.addWidget(self.btn_util_base64)

        self.btn_util_ascii = QPushButton(self.scrollAreaWidgetContents)
        self.btn_util_ascii.setObjectName(u"btn_util_ascii")

        self.verticalLayout.addWidget(self.btn_util_ascii)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout.addWidget(self.scrollArea, 0, 1, 2, 1)

        self.tabWidget.addTab(self.tab, "")

        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 756, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.btn_util_hex.setText(QCoreApplication.translate("MainWindow", u"hex", None))
        self.btn_util_decimal.setText(QCoreApplication.translate("MainWindow", u"decimal", None))
        self.btn_util_binuary.setText(QCoreApplication.translate("MainWindow", u"biunary", None))
        self.btn_util_base64.setText(QCoreApplication.translate("MainWindow", u"base64", None))
        self.btn_util_ascii.setText(QCoreApplication.translate("MainWindow", u"ascii", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"\ubcc0\ud658\uae30", None))
    # retranslateUi

