from PyQt5.QtWidgets import QMainWindow,QListWidgetItem,QTableWidgetItem,QInputDialog,QPushButton,QWidget,QTabBar
from PyQt5.QtGui import QPixmap,QIcon,QColor
from Model.DrawEnums import StateTypes
from Service import DrawService,AuthService
from Service.Model.Token import Token
from Service.Model.UserAndToken import UserAndToken

from UI.QtUI import Ui_DrawView
from UI.LayerBox import LayerBox
from UI.DrawScene import DrawScene
from UI.Models.DrawBoxEditButton import DrawBoxEditButton
from UI.Models.DrawBoxDeleteButton import DrawBoxDeleteButton
from UI.TabWidgetBox import TabWidgetBox
from Commands import CommandPanel, CommandEnums
from Model import DrawBox
from UI.Models import TabWidget

class DrawView(QMainWindow):
    __selecetedCommandP:CommandPanel
    __commandPanels:dict[int,CommandPanel]={}
    __drawService:DrawService
    __drawLayer:list[TabWidget]
    __isStartDraw:bool=False
    __selectedDrawLayerId:int

    @property
    def selectedCommandP(self) -> CommandPanel: return self.__selecetedCommandP
    @selectedCommandP.setter
    def selectedCommandP(self,commandPanel:CommandPanel):self.__selecetedCommandP=commandPanel


    def __init__(self,auth:AuthService):
        super(DrawView, self).__init__()
        self.ui = Ui_DrawView()
        self.ui.setupUi(self)
        self.__auth=auth
        self.__userAndToken=self.__auth.userAndToken
        self.__token = self.__auth.userAndToken.token

        self.__drawService:DrawService=DrawService(self.__token)

        # self.settingGraphicsView()
        self.connectButtons()
        self.setButtonsDisable(True)

        
        self.__drawBoxes:list[DrawBox]= self.__drawService.getDrawBoxes()
        
        self.getDrawBoxItems()

        self.layerBox=LayerBox(self)

        self.settingDrawBox()
        
        self.ui.cbxLayers.currentTextChanged.connect(self.changeLayer)

        self.ui.twDrawTabs.currentChanged.connect(self.test)

        self.ui.actionUserEmail.setText(self.__userAndToken.email)

        self.ui.ElementsImformation.hide()

        

    def test(self,ev):
        print(self.ui.twDrawTabs.tabText(ev))
        if self.ui.twDrawTabs.tabText(ev)=="+" and self.__isStartDraw==True:
            drawLayer=TabWidget()
            tabId=self.ui.twDrawTabs.addTab(drawLayer,"Draw Name")
            self.ui.twDrawTabs.setCurrentIndex(tabId)
            self.__isStartDraw=False
            # text, ok = QInputDialog.getText(self, 'Draw Name', 'Draw Name?')
            # if ok:
            #     if text=="":text="draw"

    #region GraphicsView

    def settingGraphicsView(self):
        self.__drawScene = DrawScene(self)
        self.__graphicView = self.ui.gvGraphicsView
        self.__graphicView.setMouseTracking(True)
        self.__graphicView.setScene(self.__drawScene)
        self.__graphicView.setVisible(False)

        self.__drawScene.MovedMouse.connect(self.mousePosition)

    #endregion
    
    #region Services and CommandPanel
    def saveDraw(self,event):self.selectedCommandP.saveDraw()
    
    def startCommand(self, command: CommandEnums):
        self.__selecetedCommandP.startCommand(command)

    def logout(self):
        self.__auth.logout()
        self.close()
    #endregion
    
    #region DrawScene

    def mousePosition(self,pos):
        self.ui.lblXCoordinate.setText(f"{round(pos.x(),4)}")
        self.ui.lblYcoordinate.setText(f"{round(pos.y(),4)}")

    def showDraw(self):
        self.setButtonsDisable(False)
        self.ui.twDrawBoxes.setVisible(False)
        self.__graphicView.setVisible(True)
        self.ui.btnAddDraw.hide()
        self.ui.btnSaveDraw.hide()

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
        __selectedIndex = self.ui.twDrawBoxes.currentRow()
        __selectedDrawBoxId=self.__drawBoxes[__selectedIndex].id
        __selectedDrawBox=self.__drawBoxes[__selectedIndex]
        
        if(__selectedDrawBoxId in self.__commandPanels):
            self.__selecetedCommandP=self.__commandPanels[__selectedDrawBoxId]
        else:
            self.__selecetedCommandP = CommandPanel(self.__drawScene,self.__token,__selectedDrawBox)
        
        self.__commandPanels[self.__selecetedCommandP.drawBox.id]=self.__selecetedCommandP
        self.showDraw()
        
        #indexi degişmeli
        self.ui.twDrawTabs.setTabText(0, self.__selecetedCommandP.drawBox.name)

        self.getLayers()

        self.__isStartDraw=True

    def settingDrawBox(self):
        self.ui.twDrawBoxes.doubleClicked.connect(self.drawDoubleClicked)
        self.ui.twDrawBoxes.setColumnWidth(0,300)
        self.ui.twDrawBoxes.setColumnWidth(1,80)
        self.ui.twDrawBoxes.setColumnWidth(2,80)
        self.ui.twDrawBoxes.setColumnWidth(3,80)
        self.ui.twDrawBoxes.setColumnWidth(4,180)
        self.ui.twDrawBoxes.setColumnWidth(5,180)

    def addDrawBoxItem(self,drawBox:DrawBox,row:int):
        self.ui.twDrawBoxes.insertRow(row)
        self.ui.twDrawBoxes.setItem(row,0,QTableWidgetItem(str(f"{drawBox.name}"),QTableWidgetItem.ItemType.Type))
        self.ui.twDrawBoxes.setCellWidget(row,1,DrawBoxEditButton(drawBox,self.getDrawBoxItems))
        self.ui.twDrawBoxes.setCellWidget(row,2,DrawBoxDeleteButton(drawBox,self.getDrawBoxItems))
        self.ui.twDrawBoxes.setItem(row,3,QTableWidgetItem(str(drawBox.state.value),QTableWidgetItem.ItemType.Type))
        self.ui.twDrawBoxes.setItem(row,4,QTableWidgetItem(str(drawBox.editTime.strftime("%m-%d-%Y %H:%M:%S")),QTableWidgetItem.ItemType.Type))
        self.ui.twDrawBoxes.setItem(row,5,QTableWidgetItem(str(drawBox.createTime.strftime("%m-%d-%Y %H:%M:%S")),QTableWidgetItem.ItemType.Type))


    def getDrawBoxItems(self):
        self.__drawBoxes.sort(key=lambda x:x.editTime)
        row=0
        self.ui.twDrawBoxes.setRowCount(0)
        
        for i in self.__drawBoxes :
            self.addDrawBoxItem(i,row)
            row =+ 1

    def addDraw(self):
        text, ok = QInputDialog.getText(self, 'Draw Name', 'Draw Name?')
        if ok:
            if text!="":
                row=self.ui.twDrawBoxes.rowCount()+1
                drawBox=DrawBox(name=text)
                self.__drawBoxes.append(drawBox)
                if drawBox!=None:self.getDrawBoxItems()
    
    #endregion

    #region LayerBox and LayerComboBox

    def setSelectedLayerAndPen(self,index:int):
        self.__selecetedCommandP.selectedLayer=self.__selecetedCommandP.layers[index]
        self.__selecetedCommandP.selectedPen= self.__selecetedCommandP.layers[index].pen

    def layerBoxShow(self):
        self.layerBox.show(self.__selecetedCommandP)
        self.layerBox.updateLayers(self.__selecetedCommandP)

    def getLayers(self):
        self.ui.cbxLayers.clear()
        for i in self.__selecetedCommandP.layers:
            px=QPixmap(12,12)
            px.fill(QColor(i.pen.red,i.pen.green,i.pen.blue))
            self.ui.cbxLayers.addItem(QIcon(px),i.name)
        self.updateLayerBox()

    def updateLayerBox(self):
        index=self.__selecetedCommandP.layers.index(self.__selecetedCommandP.selectedLayer)
        self.ui.cbxLayers.setCurrentIndex(index)

    def changeLayer(self, event):
        self.setSelectedLayerAndPen(self.ui.cbxLayers.currentIndex())

    #endregion

    #region Buttons

    def connectButtons(self):
        self.ui.pbLayerButton.clicked.connect(self.layerBoxShow)

        self.ui.actionSave.triggered.connect(self.saveDraw)

        self.ui.actionLine.triggered.connect(
            lambda: self.startCommand(CommandEnums.line)
        )
        self.ui.actionPolyLine.triggered.connect(
            lambda:self.startCommand(CommandEnums.spline)
        )
        self.ui.actionTwoPointsCircle.triggered.connect(
            lambda: self.startCommand(CommandEnums.circleTwoPoint)
        )
        self.ui.actionCenterRadiusCircle.triggered.connect(
            lambda: self.startCommand(CommandEnums.circleCenterRadius)
        )
        self.ui.actionCircle.triggered.connect(
            lambda: self.startCommand(CommandEnums.circleCenterPoint)
        )
        self.ui.actionTreePointsCircle.triggered.connect(
            lambda: self.startCommand(CommandEnums.circleTreePoint)
        )
        self.ui.actionRectangle.triggered.connect(
            lambda: self.startCommand(CommandEnums.rectangle)
        )
        self.ui.actionEllipse.triggered.connect(
            lambda: self.startCommand(CommandEnums.ellipse)
        )
        self.ui.actionArc.triggered.connect(lambda:self.startCommand(CommandEnums.arcThreePoint))
        self.ui.actionTwoPointCenterArc.triggered.connect(lambda:self.startCommand(CommandEnums.arcCenterTwoPoint))

        self.ui.actionLogout.triggered.connect(self.logout)

        self.ui.btnAddDraw.clicked.connect(self.addDraw)
        self.ui.btnSaveDraw.clicked.connect(self.saveDraws)
        

    def setButtonsDisable(self, isDisable: bool):
        self.ui.actionLine.setDisabled(isDisable)
        self.ui.actionTwoPointsCircle.setDisabled(isDisable)
        self.ui.actionCenterRadiusCircle.setDisabled(isDisable)
        self.ui.actionCircle.setDisabled(isDisable)
        self.ui.actionPolyLine.setDisabled(isDisable)
        self.ui.actionRectangle.setDisabled(isDisable)
        self.ui.actionPolygon.setDisabled(isDisable)
        self.ui.actionSPLine.setDisabled(isDisable)
        self.ui.actionGridSnap.setDisabled(isDisable)
        self.ui.actionNearestPointSnap.setDisabled(isDisable)
        self.ui.actionIntersectionPointSnap.setDisabled(isDisable)
        self.ui.actionCenterPointSnap.setDisabled(isDisable)
        self.ui.actionMidPointSnap.setDisabled(isDisable)
        self.ui.actionEndPointSnap.setDisabled(isDisable)
        self.ui.actionOrthoMode.setDisabled(isDisable)
        self.ui.actionPolarMode.setDisabled(isDisable)
        self.ui.actionOpenElementInformationBox.setDisabled(isDisable)
        self.ui.actionOpenCommandBox.setDisabled(isDisable)
        self.ui.actionMove.setDisabled(isDisable)
        self.ui.actionCopy.setDisabled(isDisable)
        self.ui.actionRotate.setDisabled(isDisable)
        self.ui.actionScale.setDisabled(isDisable)
        self.ui.actionOffset.setDisabled(isDisable)
        self.ui.actionExtend.setDisabled(isDisable)
        self.ui.actionTrim.setDisabled(isDisable)
        self.ui.actionStrech.setDisabled(isDisable)
        self.ui.actionExplode.setDisabled(isDisable)
        self.ui.actionMirror.setDisabled(isDisable)
        self.ui.actionArc.setDisabled(isDisable)
        self.ui.actionTwoPointCenterArc.setDisabled(isDisable)
        self.ui.actionEllipse.setDisabled(isDisable)
        self.ui.actionJoin.setDisabled(isDisable)
        self.ui.actionTreePointsCircle.setDisabled(isDisable)
        self.ui.pbLayerButton.setDisabled(isDisable)

        self.ui.actionSaveAs.setDisabled(isDisable)
        self.ui.actionImport.setDisabled(isDisable)
        self.ui.actionExport.setDisabled(isDisable)
        self.ui.actionNew.setDisabled(isDisable)
        self.ui.actionOpen.setDisabled(isDisable)

    #endregion
