# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/QtDesignerUI/DeleteElementBox.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DeleteElementBox(object):
    def setupUi(self, DeleteElement):
        DeleteElement.setObjectName("DeleteElement")
        DeleteElement.resize(277, 263)
        DeleteElement.setSizeGripEnabled(False)
        DeleteElement.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(DeleteElement)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Delete = QtWidgets.QRadioButton(DeleteElement)
        self.Delete.setObjectName("Delete")
        self.verticalLayout.addWidget(self.Delete)
        self.Transfer = QtWidgets.QRadioButton(DeleteElement)
        self.Transfer.setObjectName("Transfer")
        self.verticalLayout.addWidget(self.Transfer)
        self.LayerList = QtWidgets.QListWidget(DeleteElement)
        self.LayerList.setObjectName("LayerList")
        self.verticalLayout.addWidget(self.LayerList)
        self.Result = QtWidgets.QDialogButtonBox(DeleteElement)
        self.Result.setOrientation(QtCore.Qt.Horizontal)
        self.Result.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.Result.setCenterButtons(False)
        self.Result.setObjectName("Result")
        self.verticalLayout.addWidget(self.Result)

        self.retranslateUi(DeleteElement)
        self.Result.accepted.connect(DeleteElement.accept) # type: ignore
        self.Result.rejected.connect(DeleteElement.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(DeleteElement)

    def retranslateUi(self, DeleteElement):
        _translate = QtCore.QCoreApplication.translate
        DeleteElement.setWindowTitle(_translate("DeleteElement", "Delete Element"))
        self.Delete.setText(_translate("DeleteElement", "Delete Elements"))
        self.Transfer.setText(_translate("DeleteElement", "Transfer Elements Layer"))
