
from PyQt5.QtCore import QPointF
from Service import DrawService
from Service.Model import Token
from UI import DrawScene
from Commands.CommandEnums import CommandEnums
from Commands.ElementDraw import ElementDraw
from Helpers.Preview import PreviewObject
from Helpers.Snap import SnapElement,SnapSquare


class CommandPanel:
    def __init__(self, drawScene: DrawScene,token:Token) -> None:
        self.__drawScene = drawScene
        self.__isStartCommand: bool = False
        self.__token=token

        self.__snap:SnapElement=SnapElement(self.__drawScene)
        self.__elementDraw:ElementDraw = ElementDraw(self.__drawScene)
        self.__drawService:DrawService=DrawService.DrawService(self.__token)


        self.__snapObject=SnapSquare(self.__drawScene)
        self.__drawScene.addItem(self.__snapObject)

        self.__preview = PreviewObject()
        self.__drawScene.addItem(self.__preview)

        drawScene.ClickedMouse.connect(self.addCoordinate)
        drawScene.MovedMouse.connect(self.mouseMove)

        self.radius:float=10
        
        

    def mouseMove(self, scenePos):
        self.__preview.setMousePosition(scenePos)
        self.__drawScene.updateScene()
        self.__snap.snapPoints(scenePos)

    def startCommand(self, command: CommandEnums, userDrawBoxId: int, userLayerId: int):
        # self.__drawService.startCommand(command, userDrawBoxId, userLayerId)
        self.__preview.setElementType(command.value)
        self.__isStartCommand = True

    def addCoordinate(self, coordinate):
        # print(coordinate)
        if self.__isStartCommand == True:
            if (self.__snap.getSnapPoint()!=None):
                self.__preview.addPoint(self.__snap.getSnapPoint())
            else:
                # element = self.__drawService.addCoordinate(coordinate.x(), coordinate.y(), 1, 0)
                self.__preview.addPoint(coordinate)

                # if type(element) == Element:
                #     self.__elementDraw.drawElement(element)
                #     self.__preview.stop()
                #     self.__isStartCommand = False
                # else:
                #     print(element)

    def getLayers(self, drawBoxId: int):
        self.layers=self.__drawService.getLayers(drawBoxId)
        return self.layers

    def getElements(self, drawBoxId: int):
        elements = self.__drawService.getElementsWithItsLayer(drawBoxId)
        for element in elements:
            for i in self.layers:
                if(i.layerId==element.layerId):element.layer=i

        
        for i in elements:
            print(i.to_dict())
        for element in elements:self.__elementDraw.drawElement(element)
