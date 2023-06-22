from PyQt5.QtWidgets import *
from Commands.CommandPanel import CommandPanel
from Model import DrawBox
from Service.Model import Token
from UI.GraphicsView import GraphicsView
from UI.DrawScene import DrawScene
from CrossCuttingConcers.Handling.UIErrorHandle import UIErrorHandle
from Core.Signal import DrawSignal

class TabWidget2(QWidget):
    mousePositionSignal=DrawSignal(object)
    stopCommanSignal=DrawSignal()
    changeSelectObjectsSignal=DrawSignal(list)
    updateElement=DrawSignal(object)
    clickMouse=DrawSignal(object)
    __drawBox:DrawBox
    __commandPanel:CommandPanel
    __isSaved:bool=True
    __isStartCommand:bool=False
    @property
    def isSaved(self)-> bool:return  self.__isSaved
    @isSaved.setter
    def isSaved(self,isSaved:bool):self.__isSaved=isSaved

    @property
    def isStartCommand(self) -> bool: return self.__isStartCommand

    @isStartCommand.setter
    def isStartCommand(self, isStartCommand: bool): self.__isStartCommand = isStartCommand


    @property
    def commandPanel(self)->CommandPanel:return self.__commandPanel

    @property
    def drawBox(self)-> DrawBox: return  self.__drawBox

    @property
    def drawScene(self)->DrawScene:return self.__drawScene

    def __init__(self,drawBox:DrawBox,token:Token) -> None:
        super().__init__()
        self.__token=token
        self.__drawBox=drawBox


        self.settingView()

        self.__commandPanel = CommandPanel(self.__drawScene,self.__token,self.__drawBox)
        self.__commandPanel.stopCommandSignal.connect(self.runCommand)
        self.__commandPanel.saveDrawSignal.connect(self.saveDraw)
        self.__commandPanel.changeSelectObjectsSignal.connect(lambda x:self.changeSelectObjectsSignal.emit(x))
        self.__commandPanel.updateElement.connect(lambda x:self.updateElement.emit(x))

    def saveDraw(self,save:bool):self.isSaved=save
    def runCommand(self,run:bool):
        self.stopCommanSignal.emit()
        self.isStartCommand=run

    def mousePosition(self,pos):self.mousePositionSignal.emit(pos)

    def settingView(self):
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(3,3,3,3)
        self.gvGraphicsView = GraphicsView(self)
        self.gvGraphicsView.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.verticalLayout.addWidget(self.gvGraphicsView)
        self.__drawScene = DrawScene(self)
        self.__drawScene.EscOrEnterSignal.connect(lambda x:self.stopCommanSignal.emit(x))
        self.__drawScene.ClickedMouse.connect(lambda x:self.clickMouse.emit(x))
        self.gvGraphicsView.setMouseTracking(True)
        self.gvGraphicsView.setScene(self.__drawScene)
        self.__drawScene.MovedMouse.connect(self.mousePosition)


