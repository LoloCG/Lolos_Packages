# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'designerrJcVzA.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
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
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenu, QMenuBar,
    QSizePolicy, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(600, 475)
        self.actionMusic = QAction(MainWindow)
        self.actionMusic.setObjectName(u"actionMusic")
        self.actionMovie = QAction(MainWindow)
        self.actionMovie.setObjectName(u"actionMovie")
        self.actionSeries = QAction(MainWindow)
        self.actionSeries.setObjectName(u"actionSeries")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        #MainWindow.setCentralWidget(self.centralwidget) # Not sure why i need to comment this, otherwise it doesnt work
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 600, 22))
        self.menuSettings = QMenu(self.menuBar)
        self.menuSettings.setObjectName(u"menuSettings")
        self.menuAdd_new = QMenu(self.menuBar)
        self.menuAdd_new.setObjectName(u"menuAdd_new")
        self.menuAbout = QMenu(self.menuBar)
        self.menuAbout.setObjectName(u"menuAbout")
        #MainWindow.setMenuBar(self.menuBar) # Not sure why i need to comment this, otherwise it doesnt work

        self.menuBar.addAction(self.menuAdd_new.menuAction())
        self.menuBar.addAction(self.menuSettings.menuAction())
        self.menuBar.addAction(self.menuAbout.menuAction())
        self.menuAdd_new.addAction(self.actionMusic)
        self.menuAdd_new.addAction(self.actionMovie)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionMusic.setText(QCoreApplication.translate("MainWindow", u"Music", None))
        self.actionMovie.setText(QCoreApplication.translate("MainWindow", u"Films/Series", None))
        self.menuSettings.setTitle(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.menuAdd_new.setTitle(QCoreApplication.translate("MainWindow", u"Add new", None))
        self.menuAbout.setTitle(QCoreApplication.translate("MainWindow", u"About", None))
    # retranslateUi

