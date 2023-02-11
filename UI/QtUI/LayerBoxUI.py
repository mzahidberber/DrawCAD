# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/QtDesignerUI/LayerBox.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LayerBox(object):
    def setupUi(self, EditLayer):
        EditLayer.setObjectName("EditLayer")
        EditLayer.resize(550, 300)
        EditLayer.setSizeGripEnabled(False)
        EditLayer.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(EditLayer)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.AddLayer = QtWidgets.QPushButton(EditLayer)
        self.AddLayer.setObjectName("AddLayer")
        self.horizontalLayout_2.addWidget(self.AddLayer)
        self.RemoveLayer = QtWidgets.QPushButton(EditLayer)
        self.RemoveLayer.setObjectName("RemoveLayer")
        self.horizontalLayout_2.addWidget(self.RemoveLayer)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.LayerList = QtWidgets.QTableWidget(EditLayer)
        self.LayerList.setAutoScrollMargin(16)
        self.LayerList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.LayerList.setAlternatingRowColors(False)
        self.LayerList.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.LayerList.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.LayerList.setTextElideMode(QtCore.Qt.ElideRight)
        self.LayerList.setShowGrid(True)
        self.LayerList.setGridStyle(QtCore.Qt.DashLine)
        self.LayerList.setWordWrap(True)
        self.LayerList.setCornerButtonEnabled(True)
        self.LayerList.setRowCount(0)
        self.LayerList.setColumnCount(7)
        self.LayerList.setObjectName("LayerList")
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.LayerList.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.LayerList.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.LayerList.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.LayerList.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.LayerList.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.LayerList.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.LayerList.setHorizontalHeaderItem(6, item)
        self.LayerList.horizontalHeader().setVisible(True)
        self.LayerList.horizontalHeader().setCascadingSectionResizes(False)
        self.LayerList.horizontalHeader().setHighlightSections(False)
        self.LayerList.horizontalHeader().setSortIndicatorShown(True)
        self.LayerList.horizontalHeader().setStretchLastSection(False)
        self.LayerList.verticalHeader().setVisible(True)
        self.LayerList.verticalHeader().setCascadingSectionResizes(False)
        self.LayerList.verticalHeader().setDefaultSectionSize(20)
        self.LayerList.verticalHeader().setHighlightSections(False)
        self.LayerList.verticalHeader().setMinimumSectionSize(20)
        self.verticalLayout.addWidget(self.LayerList)

        self.retranslateUi(EditLayer)
        QtCore.QMetaObject.connectSlotsByName(EditLayer)

    def retranslateUi(self, EditLayer):
        _translate = QtCore.QCoreApplication.translate
        EditLayer.setWindowTitle(_translate("EditLayer", "Edit Layer"))
        self.AddLayer.setText(_translate("EditLayer", "Add"))
        self.RemoveLayer.setText(_translate("EditLayer", "Remove"))
        self.LayerList.setSortingEnabled(True)
        item = self.LayerList.horizontalHeaderItem(0)
        item.setText(_translate("EditLayer", "Name"))
        item = self.LayerList.horizontalHeaderItem(1)
        item.setText(_translate("EditLayer", "Lock"))
        item = self.LayerList.horizontalHeaderItem(2)
        item.setText(_translate("EditLayer", "Visibility"))
        item = self.LayerList.horizontalHeaderItem(3)
        item.setText(_translate("EditLayer", "Thickness"))
        item = self.LayerList.horizontalHeaderItem(4)
        item.setText(_translate("EditLayer", "Color"))
        item = self.LayerList.horizontalHeaderItem(5)
        item.setText(_translate("EditLayer", "Type"))
        item = self.LayerList.horizontalHeaderItem(6)
        item.setText(_translate("EditLayer", "Elements "))
