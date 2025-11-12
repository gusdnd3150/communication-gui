# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'utilty.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QHeaderView, QLabel, QLineEdit, QMainWindow,
    QMenuBar, QPushButton, QScrollArea, QSizePolicy,
    QStatusBar, QTabWidget, QTableWidget, QTableWidgetItem,
    QTextEdit, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1129, 727)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_3 = QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout = QGridLayout(self.tab)
        self.gridLayout.setObjectName(u"gridLayout")
        self.scrollArea = QScrollArea(self.tab)
        self.scrollArea.setObjectName(u"scrollArea")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setMinimumSize(QSize(100, 0))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 98, 623))
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

        self.line = QFrame(self.scrollAreaWidgetContents)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.btn_short_big = QPushButton(self.scrollAreaWidgetContents)
        self.btn_short_big.setObjectName(u"btn_short_big")

        self.verticalLayout.addWidget(self.btn_short_big)

        self.btn_double_big = QPushButton(self.scrollAreaWidgetContents)
        self.btn_double_big.setObjectName(u"btn_double_big")

        self.verticalLayout.addWidget(self.btn_double_big)

        self.btn_int_big = QPushButton(self.scrollAreaWidgetContents)
        self.btn_int_big.setObjectName(u"btn_int_big")

        self.verticalLayout.addWidget(self.btn_int_big)

        self.btn_float_big = QPushButton(self.scrollAreaWidgetContents)
        self.btn_float_big.setObjectName(u"btn_float_big")

        self.verticalLayout.addWidget(self.btn_float_big)

        self.line_2 = QFrame(self.scrollAreaWidgetContents)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.btn_short_little = QPushButton(self.scrollAreaWidgetContents)
        self.btn_short_little.setObjectName(u"btn_short_little")

        self.verticalLayout.addWidget(self.btn_short_little)

        self.btn_double_little = QPushButton(self.scrollAreaWidgetContents)
        self.btn_double_little.setObjectName(u"btn_double_little")

        self.verticalLayout.addWidget(self.btn_double_little)

        self.btn_int_little = QPushButton(self.scrollAreaWidgetContents)
        self.btn_int_little.setObjectName(u"btn_int_little")
        self.btn_int_little.setStyleSheet(u"")

        self.verticalLayout.addWidget(self.btn_int_little)

        self.btn_float_little = QPushButton(self.scrollAreaWidgetContents)
        self.btn_float_little.setObjectName(u"btn_float_little")

        self.verticalLayout.addWidget(self.btn_float_little)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout.addWidget(self.scrollArea, 0, 1, 3, 1)

        self.util_combo = QComboBox(self.tab)
        self.util_combo.setObjectName(u"util_combo")

        self.gridLayout.addWidget(self.util_combo, 0, 0, 1, 1)

        self.util_text = QTextEdit(self.tab)
        self.util_text.setObjectName(u"util_text")

        self.gridLayout.addWidget(self.util_text, 1, 0, 2, 1)

        self.tabWidget_2 = QTabWidget(self.tab)
        self.tabWidget_2.setObjectName(u"tabWidget_2")
        self.text = QWidget()
        self.text.setObjectName(u"text")
        self.gridLayout_2 = QGridLayout(self.text)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.util_encode = QTextEdit(self.text)
        self.util_encode.setObjectName(u"util_encode")

        self.gridLayout_2.addWidget(self.util_encode, 0, 0, 1, 1)

        self.tabWidget_2.addTab(self.text, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.gridLayout_4 = QGridLayout(self.tab_3)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.util_encode_table = QTableWidget(self.tab_3)
        self.util_encode_table.setObjectName(u"util_encode_table")

        self.gridLayout_4.addWidget(self.util_encode_table, 0, 0, 1, 1)

        self.tabWidget_2.addTab(self.tab_3, "")

        self.gridLayout.addWidget(self.tabWidget_2, 0, 2, 3, 1)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.gridLayout_6 = QGridLayout(self.tab_2)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.pre_text = QTextEdit(self.tab_2)
        self.pre_text.setObjectName(u"pre_text")

        self.verticalLayout_2.addWidget(self.pre_text)

        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.total_length = QLineEdit(self.tab_2)
        self.total_length.setObjectName(u"total_length")

        self.gridLayout_5.addWidget(self.total_length, 0, 1, 1, 1)

        self.divied_length = QLineEdit(self.tab_2)
        self.divied_length.setObjectName(u"divied_length")

        self.gridLayout_5.addWidget(self.divied_length, 0, 3, 1, 1)

        self.label_2 = QLabel(self.tab_2)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_5.addWidget(self.label_2, 0, 2, 1, 1)

        self.label = QLabel(self.tab_2)
        self.label.setObjectName(u"label")

        self.gridLayout_5.addWidget(self.label, 0, 0, 1, 1)

        self.run_divied = QPushButton(self.tab_2)
        self.run_divied.setObjectName(u"run_divied")

        self.gridLayout_5.addWidget(self.run_divied, 0, 4, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout_5)

        self.next_text = QTextEdit(self.tab_2)
        self.next_text.setObjectName(u"next_text")

        self.verticalLayout_2.addWidget(self.next_text)


        self.gridLayout_6.addLayout(self.verticalLayout_2, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_2, "")

        self.gridLayout_3.addWidget(self.tabWidget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1129, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.btn_util_hex.setText(QCoreApplication.translate("MainWindow", u"hex", None))
        self.btn_util_decimal.setText(QCoreApplication.translate("MainWindow", u"decimal", None))
        self.btn_util_binuary.setText(QCoreApplication.translate("MainWindow", u"biunary", None))
        self.btn_util_base64.setText(QCoreApplication.translate("MainWindow", u"base64", None))
        self.btn_util_ascii.setText(QCoreApplication.translate("MainWindow", u"ascii (\ubb38\uc790)", None))
        self.btn_short_big.setText(QCoreApplication.translate("MainWindow", u"Short B (2)", None))
        self.btn_double_big.setText(QCoreApplication.translate("MainWindow", u"Double B (8)", None))
        self.btn_int_big.setText(QCoreApplication.translate("MainWindow", u"int B(4)", None))
        self.btn_float_big.setText(QCoreApplication.translate("MainWindow", u"Float B(4)", None))
        self.btn_short_little.setText(QCoreApplication.translate("MainWindow", u"Short L (2)", None))
        self.btn_double_little.setText(QCoreApplication.translate("MainWindow", u"Double L (8)", None))
        self.btn_int_little.setText(QCoreApplication.translate("MainWindow", u"int L(4)", None))
        self.btn_float_little.setText(QCoreApplication.translate("MainWindow", u"Float L(4)", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.text), QCoreApplication.translate("MainWindow", u"text", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"table", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"\ubcc0\ud658\uae30", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\ud328\ud0b7 \ubcc4 \ubd84\ud560\uae38\uc774(, \uad6c\ubd84\uc790)", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\ud328\ud0b7 \ud558\ub098\ub2f9 \ucd1d\uae38\uc774", None))
        self.run_divied.setText(QCoreApplication.translate("MainWindow", u"\ubd84\ud560", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"\ubb38\uc790 \uae38\uc774 \ubd84\ud560\uae30", None))
    # retranslateUi

