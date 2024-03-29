# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/QtDesignerUI/tabWidget.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TabWidget(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(836, 567)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btnAddDraw = QtWidgets.QPushButton(Form)
        self.btnAddDraw.setMaximumSize(QtCore.QSize(100, 16777215))
        self.btnAddDraw.setObjectName("btnAddDraw")
        self.horizontalLayout_3.addWidget(self.btnAddDraw)
        self.btnSaveDraw = QtWidgets.QPushButton(Form)
        self.btnSaveDraw.setMaximumSize(QtCore.QSize(100, 16777215))
        self.btnSaveDraw.setObjectName("btnSaveDraw")
        self.horizontalLayout_3.addWidget(self.btnSaveDraw)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.twDrawBoxes = QtWidgets.QTableWidget(Form)
        self.twDrawBoxes.setObjectName("twDrawBoxes")
        self.twDrawBoxes.setColumnCount(6)
        self.twDrawBoxes.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.twDrawBoxes.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.twDrawBoxes.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.twDrawBoxes.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.twDrawBoxes.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.twDrawBoxes.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.twDrawBoxes.setHorizontalHeaderItem(5, item)
        self.verticalLayout.addWidget(self.twDrawBoxes)
        self.gvGraphicsView = GraphicsView(Form)
        self.gvGraphicsView.setMouseTracking(False)
        self.gvGraphicsView.setViewportUpdateMode(QtWidgets.QGraphicsView.FullViewportUpdate)
        self.gvGraphicsView.setObjectName("gvGraphicsView")
        self.verticalLayout.addWidget(self.gvGraphicsView)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.btnAddDraw.setText(_translate("Form", "Add"))
        self.btnSaveDraw.setText(_translate("Form", "Save"))
        item = self.twDrawBoxes.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Name"))
        item = self.twDrawBoxes.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Edit Name"))
        item = self.twDrawBoxes.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Delete"))
        item = self.twDrawBoxes.horizontalHeaderItem(3)
        item.setText(_translate("Form", "State"))
        item = self.twDrawBoxes.horizontalHeaderItem(4)
        item.setText(_translate("Form", "Edit Time"))
        item = self.twDrawBoxes.horizontalHeaderItem(5)
        item.setText(_translate("Form", "Create Time"))

from UI.GraphicsView import GraphicsView
