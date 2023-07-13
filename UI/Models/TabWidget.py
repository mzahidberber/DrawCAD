from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, Qt
from Commands.CommandPanel import CommandPanel
from Model import DrawBox
from Model.DrawEnums import StateTypes
from Service import DrawService
from Service.Model import Token
from UI.GraphicsView import GraphicsView
from UI.DrawScene import DrawScene
from UI.Models import DrawBoxDeleteButton, DrawBoxEditButton
from Core.Signal import DrawSignal

class TabWidget(QWidget):
    mousePositionSignal=DrawSignal(object)
    selectDrawSignal=DrawSignal(object)

    __commandPanel:CommandPanel


    @property
    def commandPanel(self)->CommandPanel:return self.__commandPanel


    def __init__(self,drawService:DrawService,drawBoxes:list[DrawBox],token:Token) -> None:
        super().__init__()
        self.__drawService=drawService
        self.__drawBoxes=drawBoxes
        self.__token=token
        self.settingView()
        self.settingGraphicsView()

        # self.__drawBoxes:list[DrawBox]= self.__drawService.getDrawBoxes()

        self.getDrawBoxItems()

        self.settingDrawBox()

        self.btnAddDraw.clicked.connect(self.addDraw)
        self.btnSaveDraw.clicked.connect(self.saveDraws)

    def closeEvent(self, a0) -> None:
        return super().closeEvent(a0)

    def settingGraphicsView(self):
        self.__drawScene = DrawScene(self)
        self.__graphicView = self.gvGraphicsView
        self.__graphicView.setMouseTracking(True)
        self.__graphicView.setScene(self.__drawScene)
        self.__graphicView.setVisible(False)

        self.__drawScene.MovedMouse.connect(self.mousePosition)

    def mousePosition(self,pos):self.mousePositionSignal.emit(pos)

    #region DrawScene

    def showDraw(self):
        self.twDrawBoxes.setVisible(False)
        self.__graphicView.setVisible(True)
        self.btnAddDraw.hide()
        self.btnSaveDraw.hide()

    #endregion

    #region DrawBox

    def saveDraws(self):
        addList=list(filter(lambda d:d.state==StateTypes.added,self.__drawBoxes))
        deleteList=list(filter(lambda d:d.state==StateTypes.delete,self.__drawBoxes))
        updatelist=list(filter(lambda d:d.state==StateTypes.update,self.__drawBoxes))
        deleteListIds=list(map(lambda d:d.id,deleteList))
        list(filter(lambda d:self.__drawBoxes.remove(d),deleteList))
        newDrawBoxes=self.__drawService.addDraw(addList)
        self.__drawService.updateDrawBoxes(updatelist)
        self.__drawService.deleteDrawBoxes(deleteListIds)

        for i in addList:self.__drawBoxes.remove(i)
        if newDrawBoxes!=None:
            for i in newDrawBoxes:self.__drawBoxes.append(i) 
        for i in updatelist:i.state=StateTypes.unchanged
        
        self.getDrawBoxItems()

    def drawDoubleClicked(self, event):
        __selectedIndex = self.twDrawBoxes.currentRow()
        __selectedDrawBox=self.__drawBoxes[__selectedIndex]
        if not __selectedDrawBox.isStart:
            self.__commandPanel = CommandPanel(self.__drawScene,self.__token,__selectedDrawBox)
            self.showDraw()
        
            self.selectDrawSignal.emit(__selectedDrawBox)
            __selectedDrawBox.isStart=True

    def settingDrawBox(self):
        self.twDrawBoxes.doubleClicked.connect(self.drawDoubleClicked)
        self.twDrawBoxes.setColumnWidth(0,300)
        self.twDrawBoxes.setColumnWidth(1,80)
        self.twDrawBoxes.setColumnWidth(2,80)
        self.twDrawBoxes.setColumnWidth(3,80)
        self.twDrawBoxes.setColumnWidth(4,80)
        self.twDrawBoxes.setColumnWidth(5,180)
        self.twDrawBoxes.setColumnWidth(6,180)

    def addDrawBoxItem(self,drawBox:DrawBox,row:int):
        self.twDrawBoxes.insertRow(row)
        self.twDrawBoxes.setItem(row,0,QTableWidgetItem(str(f"{drawBox.name}"),QTableWidgetItem.ItemType.Type))
        self.twDrawBoxes.setCellWidget(row,1,DrawBoxEditButton(drawBox,self.getDrawBoxItems))
        self.twDrawBoxes.setCellWidget(row,2,DrawBoxDeleteButton(drawBox,self.getDrawBoxItems))
        self.twDrawBoxes.setItem(row,3,QTableWidgetItem(str(drawBox.state.value),QTableWidgetItem.ItemType.Type))
        self.twDrawBoxes.setItem(row,4,QTableWidgetItem(str(drawBox.isStart),QTableWidgetItem.ItemType.Type))
        self.twDrawBoxes.setItem(row,5,QTableWidgetItem(str(drawBox.editTime.strftime("%m-%d-%Y %H:%M:%S")),QTableWidgetItem.ItemType.Type))
        self.twDrawBoxes.setItem(row,6,QTableWidgetItem(str(drawBox.createTime.strftime("%m-%d-%Y %H:%M:%S")),QTableWidgetItem.ItemType.Type))

        for column in range(0,self.twDrawBoxes.columnCount()):
            item=self.twDrawBoxes.item(row,column)
            if item !=None:item.setFlags(Qt.ItemIsEnabled)


    def getDrawBoxItems(self):
        self.__drawBoxes.sort(key=lambda x:x.editTime)
        row=0
        self.twDrawBoxes.setRowCount(0)
        
        for i in self.__drawBoxes :
            self.addDrawBoxItem(i,row)
            if i.isStart==True:
                for column in range(0,self.twDrawBoxes.columnCount()):
                    cellwidget=self.twDrawBoxes.cellWidget(row,column)
                    if cellwidget != None:cellwidget.setEnabled(False)
                    item=self.twDrawBoxes.item(row,column)
                    if item !=None:item.setFlags(Qt.ItemIsEnabled)
            row =+ 1

    def addDraw(self):
        text, ok = QInputDialog.getText(self, 'Draw Name', 'Draw Name?')
        if ok:
            if text!="":
                row=self.twDrawBoxes.rowCount()+1
                drawBox=DrawBox(name=text)
                self.__drawBoxes.append(drawBox)
                if drawBox!=None:self.getDrawBoxItems()
    
    #endregion

    def settingView(self):
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btnAddDraw = QPushButton(self)
        self.btnAddDraw.setMaximumSize(QSize(100, 16777215))
        self.btnAddDraw.setObjectName("btnAddDraw")
        self.horizontalLayout_3.addWidget(self.btnAddDraw)
        self.btnSaveDraw = QPushButton(self)
        self.btnSaveDraw.setMaximumSize(QSize(100, 16777215))
        self.btnSaveDraw.setObjectName("btnSaveDraw")
        self.horizontalLayout_3.addWidget(self.btnSaveDraw)
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding,QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.twDrawBoxes = QTableWidget(self)
        self.twDrawBoxes.setObjectName("twDrawBoxes")
        self.twDrawBoxes.setColumnCount(7)
        self.twDrawBoxes.setRowCount(0)
        item = QTableWidgetItem()
        self.twDrawBoxes.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.twDrawBoxes.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.twDrawBoxes.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        self.twDrawBoxes.setHorizontalHeaderItem(3, item)
        item = QTableWidgetItem()
        self.twDrawBoxes.setHorizontalHeaderItem(4, item)
        item = QTableWidgetItem()
        self.twDrawBoxes.setHorizontalHeaderItem(5, item)
        item = QTableWidgetItem()
        self.twDrawBoxes.setHorizontalHeaderItem(6, item)
        self.verticalLayout.addWidget(self.twDrawBoxes)
        self.gvGraphicsView = GraphicsView(self)
        self.gvGraphicsView.setMouseTracking(False)
        self.gvGraphicsView.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.gvGraphicsView.setObjectName("gvGraphicsView")
        self.verticalLayout.addWidget(self.gvGraphicsView)


        self.btnAddDraw.setText("Add")
        self.btnSaveDraw.setText("Save")
        item = self.twDrawBoxes.horizontalHeaderItem(0)
        item.setSelected(False)
        item.setText("Name")
        item = self.twDrawBoxes.horizontalHeaderItem(1)
        item.setSelected(False)
        item.setText("Edit Name")
        item = self.twDrawBoxes.horizontalHeaderItem(2)
        item.setSelected(False)
        item.setText("Delete")
        item = self.twDrawBoxes.horizontalHeaderItem(3)
        item.setSelected(False)
        item.setText("State")
        item = self.twDrawBoxes.horizontalHeaderItem(4)
        item.setSelected(False)
        item.setText("Open")
        item = self.twDrawBoxes.horizontalHeaderItem(5)
        item.setSelected(False)
        item.setText("Edit Time")
        item = self.twDrawBoxes.horizontalHeaderItem(6)
        item.setSelected(False)
        item.setText("Create Time")