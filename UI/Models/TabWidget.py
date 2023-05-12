from PyQt5 import QtWidgets,QtCore
from PyQt5.QtCore import pyqtSignal
from UI.GraphicsView import GraphicsView
from UI.DrawScene import DrawScene
class TabWidget(QtWidgets.QWidget):
    mousePositionSignal=pyqtSignal(object)

    def __init__(self) -> None:
        super().__init__()
        
        self.settingView()
        self.settingGraphicsView()

    def settingGraphicsView(self):
        self.__drawScene = DrawScene(self)
        self.__graphicView = self.gvGraphicsView
        self.__graphicView.setMouseTracking(True)
        self.__graphicView.setScene(self.__drawScene)
        self.__graphicView.setVisible(False)

        self.__drawScene.MovedMouse.connect(self.mousePosition)

    def mousePosition(self,pos):self.mousePositionSignal.emit(pos)


    def settingView(self):
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btnAddDraw = QtWidgets.QPushButton(self)
        self.btnAddDraw.setMaximumSize(QtCore.QSize(100, 16777215))
        self.btnAddDraw.setObjectName("btnAddDraw")
        self.horizontalLayout_3.addWidget(self.btnAddDraw)
        self.btnSaveDraw = QtWidgets.QPushButton(self)
        self.btnSaveDraw.setMaximumSize(QtCore.QSize(100, 16777215))
        self.btnSaveDraw.setObjectName("btnSaveDraw")
        self.horizontalLayout_3.addWidget(self.btnSaveDraw)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.twDrawBoxes = QtWidgets.QTableWidget(self)
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
        self.gvGraphicsView = GraphicsView(self)
        self.gvGraphicsView.setMouseTracking(False)
        self.gvGraphicsView.setViewportUpdateMode(QtWidgets.QGraphicsView.FullViewportUpdate)
        self.gvGraphicsView.setObjectName("gvGraphicsView")
        self.verticalLayout.addWidget(self.gvGraphicsView)


        self.btnAddDraw.setText("Add")
        self.btnSaveDraw.setText("Save")
        item = self.twDrawBoxes.horizontalHeaderItem(0)
        item.setText("Name")
        item = self.twDrawBoxes.horizontalHeaderItem(1)
        item.setText("Edit Name")
        item = self.twDrawBoxes.horizontalHeaderItem(2)
        item.setText("Delete")
        item = self.twDrawBoxes.horizontalHeaderItem(3)
        item.setText("State")
        item = self.twDrawBoxes.horizontalHeaderItem(4)
        item.setText("Edit Time")
        item = self.twDrawBoxes.horizontalHeaderItem(5)
        item.setText("Create Time")