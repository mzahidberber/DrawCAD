from UI import DrawScene
from Commands.CommandEnums import CommandEnums
from Commands.ElementDraw import ElementDraw
from Model import Element
from Service import DrawService
from PyQt5.QtCore import QPointF
from Helpers.Preview import PreviewObject

class CommandPanel:
    def __init__(self,drawScene:DrawScene) -> None:
        self.__drawScene=drawScene
        self.__isStartCommand:bool=False

        self.__mouseCoordinate=QPointF(0,0)

        drawScene.ClickedMouse.connect(self.addCoordinate)
        drawScene.MovedMouse.connect(self.mouseMove)
        
        # drawTest(self.__drawScene)
    
    def mouseMove(self,scenePos):
        self.__mouseCoordinate=scenePos

    def startCommand(self,command:CommandEnums,userDrawBoxId:int,userLayerId:int):
        DrawService().startCommand(command,userDrawBoxId,userLayerId)
        self.__isStartCommand=True

    def addCoordinate(self,coordinate):
        print(coordinate)
        if (self.__isStartCommand==True):
            element=DrawService().addCoordinate(coordinate.x(),coordinate.y(),1,0)
            # self.__preview=PreviewObject(1,[coordinate,self.__mouseCoordinate])
            print(type(element))
            if(type(element)==Element):
                ElementDraw(self.__drawScene).drawElement(element)
                self.__isStartCommand=False
            else: print(element)

    def getLayers(self,drawBoxId:int):
        return DrawService().getLayers(drawBoxId)

    def getElements(self,drawBoxId:int):
        elements=DrawService().getElementsWithItsLayer(drawBoxId)
        for element in elements:
            ElementDraw(self.__drawScene).drawElement(element)