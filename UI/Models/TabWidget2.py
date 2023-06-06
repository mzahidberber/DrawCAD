from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize,pyqtSignal,Qt
from Commands.CommandPanel import CommandPanel
from Model import DrawBox
from Model.DrawEnums import StateTypes
from Service import DrawService
from Service.Model import Token
from UI.GraphicsView import GraphicsView
from UI.DrawScene import DrawScene
from UI.Models import DrawBoxDeleteButton, DrawBoxEditButton
class TabWidget2(QWidget):
    mousePositionSignal=pyqtSignal(object)
    stopCommanSignal=pyqtSignal()
    changeSelectObjectsSignal=pyqtSignal(list)
    updateElement=pyqtSignal(object)
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
        self.__commandPanel.changeSelectObjectsSignal.connect(self.changeSelectObjectsSignal)
        self.__commandPanel.updateElement.connect(self.updateElement)


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
        self.__drawScene.EscOrEnterSignal.connect(self.stopCommanSignal)
        self.gvGraphicsView.setMouseTracking(True)
        self.gvGraphicsView.setScene(self.__drawScene)
        self.__drawScene.MovedMouse.connect(self.mousePosition)
