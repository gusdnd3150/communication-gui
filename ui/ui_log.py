# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'log.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QHBoxLayout,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QTextEdit, QVBoxLayout, QWidget)

class Ui_Log(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(571, 696)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.checkBox = QCheckBox(self.centralwidget)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setGeometry(QRect(480, 220, 74, 16))
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.log_chk_showlog = QCheckBox(self.centralwidget)
        self.log_chk_showlog.setObjectName(u"log_chk_showlog")

        self.horizontalLayout_2.addWidget(self.log_chk_showlog)

        self.log_btn_clear = QPushButton(self.centralwidget)
        self.log_btn_clear.setObjectName(u"log_btn_clear")
        self.log_btn_clear.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_2.addWidget(self.log_btn_clear)


        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.log_text_log = QTextEdit(self.centralwidget)
        self.log_text_log.setObjectName(u"log_text_log")
        self.log_text_log.setLineWrapMode(QTextEdit.NoWrap)
        self.log_text_log.setReadOnly(True)
        self.log_text_log.setAcceptRichText(True)

        self.verticalLayout.addWidget(self.log_text_log)


        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 571, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"CheckBox", None))
        self.log_chk_showlog.setText(QCoreApplication.translate("MainWindow", u"show Log", None))
        self.log_btn_clear.setText(QCoreApplication.translate("MainWindow", u"clear", None))
        self.log_text_log.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Gulim'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
    # retranslateUi

