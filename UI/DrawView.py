from PyQt5.QtWidgets import QMainWindow
from Service import DrawService
from Service.Model.Token import Token

from UI.QtUI import Ui_DrawView
from UI.LayerBox import LayerBox
from UI.DrawScene import DrawScene
from Commands import CommandPanel, CommandEnums
from Model import DrawBox


class DrawView(QMainWindow):
    __selecetedCommandP:CommandPanel

    @property
    def selectedCommandP(self) -> CommandPanel: return self.__selecetedCommandP
    @selectedCommandP.setter
    def selectedCommandP(self,commandPanel:CommandPanel):self.__selecetedCommandP=commandPanel


    def __init__(self, token: Token):
        super(DrawView, self).__init__()
        self.ui = Ui_DrawView()
        self.ui.setupUi(self)
        self.__token = token

        
        self.__drawScene = DrawScene(self)
        self.__graphicView = self.ui.gvGraphicsView
        self.__graphicView.setMouseTracking(True)
        self.__graphicView.setScene(self.__drawScene)
        self.__graphicView.setVisible(False)

        self.__drawService:DrawService=DrawService(self.__token)
        self.__drawBoxes:list[DrawBox]= self.__drawService.getDrawBoxes()
        print(self.__drawBoxes)
        self.__commandPanels:dict[int,CommandPanel]={}
        self.getDrawBoxItems()

        self.layerBox=LayerBox()

        self.connectButtons()
        self.setButtonsDisable(True)
        
        self.ui.lwDrawBoxes.doubleClicked.connect(self.drawDoubleClicked)
        self.ui.cbxLayers.currentTextChanged.connect(self.changeLayer)

    def startCommand(self, command: CommandEnums):
        self.__selecetedCommandP.startCommand(command)

    def showDraw(self):
        self.setButtonsDisable(False)
        self.ui.lwDrawBoxes.setVisible(False)
        self.__graphicView.setVisible(True)

    def drawDoubleClicked(self, event):
        __selectedIndex = self.ui.lwDrawBoxes.currentRow()
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
        
        self.setSelectedLayerAndPen(self.ui.cbxLayers.currentIndex())

        
    
    
    def setSelectedLayerAndPen(self,index:int):
        self.__selecetedCommandP.selectedLayer=self.__selecetedCommandP.layers[index]
        self.__selecetedCommandP.selectedPen= self.__selecetedCommandP.layers[index].pen



    def getDrawBoxItems(self):
        for i in self.__drawBoxes :
            self.ui.lwDrawBoxes.addItem(i.name)

    def getLayers(self):
        for i in self.__selecetedCommandP.layers:
            self.ui.cbxLayers.addItem(i.name)

    def changeLayer(self, event):self.setSelectedLayerAndPen(self.ui.cbxLayers.currentIndex())
       

    

    def closeEvent(self, event):
        pass

    def saveDraw(self,event):
        self.selectedCommandP.saveDraw()

    def layerBoxShow(self):
        self.layerBox.show(self.__selecetedCommandP)
        self.layerBox.updateLayers(self.__selecetedCommandP)

    def connectButtons(self):
        self.ui.pbLayerButton.clicked.connect(self.layerBoxShow)

        self.ui.actionSave.triggered.connect(self.saveDraw)

        self.ui.actionLine.triggered.connect(
            lambda: self.startCommand(CommandEnums.line)
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

    


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = DrawView(1)
    window.show()
    sys.exit(app.exec_())
