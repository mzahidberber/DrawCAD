from PyQt5.QtCore import QPointF
from UI import DrawScene
from Commands.CommandEnums import CommandEnums,getType
from Commands.ElementDraw import ElementDraw
from Model import Element
from Service import DrawService
from Helpers.Preview import PreviewObject


class CommandPanel:
    def __init__(self, drawScene: DrawScene) -> None:
        self.__drawScene = drawScene
        self.__isStartCommand: bool = False

        self.__elementDraw:ElementDraw = ElementDraw(self.__drawScene)
        self.__drawService:DrawService=DrawService()

        self.__preview = PreviewObject()
        self.__drawScene.addItem(self.__preview)

        drawScene.ClickedMouse.connect(self.addCoordinate)
        drawScene.MovedMouse.connect(self.mouseMove)
        
        

    def mouseMove(self, scenePos):
        self.__preview.setMousePosition(scenePos)
        self.__drawScene.updateScene()

    def startCommand(self, command: CommandEnums, userDrawBoxId: int, userLayerId: int):
        self.__drawService.startCommand(command, userDrawBoxId, userLayerId)
        self.__preview.setElementType(command.value)
        self.__isStartCommand = True

    def addCoordinate(self, coordinate):
        print(coordinate)
        if self.__isStartCommand == True:
            element = self.__drawService.addCoordinate(coordinate.x(), coordinate.y(), 1, 0)
            self.__preview.addPoint(coordinate)

            if type(element) == Element:
                self.__elementDraw.drawElement(element)
                self.__preview.stop()
                self.__isStartCommand = False
            else:
                print(element)

    def getLayers(self, drawBoxId: int):
        return self.__drawService.getLayers(drawBoxId)

    def getElements(self, drawBoxId: int):
        elements = self.__drawService.getElementsWithItsLayer(drawBoxId)
        for element in elements:self.__elementDraw.drawElement(element)
