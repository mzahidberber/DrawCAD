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
    __selectedDrawLayer:TabWidget

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
        
        self.layerBox=LayerBox(self)
        self.ui.cbxLayers.currentTextChanged.connect(self.changeLayer)
        self.ui.actionUserEmail.setText(self.__userAndToken.email)
        self.ui.ElementsImformation.hide()

        self.addDrawLayer()
        self.ui.twDrawTabs.currentChanged.connect(self.tabChange)
    
    def addDrawLayer(self):
        drawLayer=TabWidget(self.__drawService,self.__token)
        drawLayer.mousePositionSignal.connect(self.mousePosition)
        drawLayer.selectDrawSignal.connect(self.selectDraw)
        tabId=self.ui.twDrawTabs.addTab(drawLayer,"Draw Name")
        self.ui.twDrawTabs.setCurrentIndex(tabId)
        self.__selectedDrawLayerId=tabId
        self.__selectedDrawLayer=drawLayer
        

    def tabChange(self,ev):
        # print(self.ui.twDrawTabs.tabText(ev))
        if self.ui.twDrawTabs.tabText(ev)=="+" and self.__isStartDraw==True:
            self.addDrawLayer()
            self.__isStartDraw=False
        else:
            self.ui.twDrawTabs.setCurrentIndex(self.__selectedDrawLayerId)

    def mousePosition(self,pos):
        self.ui.lblXCoordinate.setText(f"{round(pos.x(),4)}")
        self.ui.lblYcoordinate.setText(f"{round(pos.y(),4)}")

    def selectDraw(self,draw:DrawBox):
        self.ui.twDrawTabs.setTabText(self.__selectedDrawLayerId,draw.name)
        self.setButtonsDisable(False)

        self.ui.cbxLayers.clear()
        for i in self.__selectedDrawLayer.commandPanel.layers:
            px=QPixmap(12,12)
            px.fill(QColor(i.pen.red,i.pen.green,i.pen.blue))
            self.ui.cbxLayers.addItem(QIcon(px),i.name)
        self.updateLayerBox()

        self.__isStartDraw=True
    
    #region Services and CommandPanel
    def saveDraw(self,event):self.selectedCommandP.saveDraw()
    
    def startCommand(self, command: CommandEnums):
        self.__selecetedCommandP.startCommand(command)

    def logout(self):
        self.__auth.logout()
        self.close()
    #endregion
    
    

    #region LayerBox and LayerComboBox

    def setSelectedLayerAndPen(self,index:int):
        self.__selectedDrawLayer.commandPanel.selectedLayer=self.__selectedDrawLayer.commandPanel.layers[index]
        self.__selectedDrawLayer.commandPanel.selectedPen= self.__selectedDrawLayer.commandPanel.layers[index].pen

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
        index=self.__selectedDrawLayer.commandPanel.layers.index(self.__selectedDrawLayer.commandPanel.selectedLayer)
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
