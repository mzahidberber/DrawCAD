from PyQt5.QtCore import QPointF
from Elements import ElementObj
from Model import DrawBox, Element, Layer, Pen, PenStyle
from Service.DrawService import DrawService
from Service.Model import Token
from UI import DrawScene
from Commands.CommandEnums import CommandEnums
from Commands.ElementDraw import ElementDraw
from Commands.DrawObjects import DrawObjects
from Helpers.Preview import PreviewObject
from Helpers.Snap import SnapElement, SnapSquare
from Model.DrawEnums import StateTypes


class CommandPanel:
    __selectedLayer:Layer
    __selectedPen:Pen
    __drawBox=DrawBox
    __drawObjs:DrawObjects
    __drawScene:DrawScene
    __elementDraw:ElementDraw
    __drawService:DrawService
    __snap:SnapElement
    __snapObject:SnapSquare
    __preview:PreviewObject

    @property
    def selectedLayer(self)-> Layer:return self.__selectedLayer
    @selectedLayer.setter
    def selectedLayer(self,layer:Layer):self.__selectedLayer=layer

    @property
    def selectedPen(self)-> Pen:return self.__selectedPen
    @selectedPen.setter
    def selectedPen(self,pen:Pen):self.__selectedPen=pen

    @property
    def drawElementObjects(self):return self.__drawObjs.elementObjs
    @drawElementObjects.setter
    def drawElementObjects(self,elements:list[ElementObj]):self.__drawObjs.elementObjs=elements

    @property
    def layers(self):return self.__drawObjs.layers
    @layers.setter
    def layers(self,layers:list[Layer]):self.__drawObjs.layers=layers
    
    @property
    def pens(self):return self.__pens
    @pens.setter
    def pens(self,pens:list[Pen]):self.__pens=pens

    @property
    def penStyles(self):return self.__drawObjs.penStyles

    @property
    def drawBox(self)->DrawBox :return self.__drawBox



    def __init__(self, drawScene: DrawScene, token: Token,drawBox:DrawBox) -> None:
        self.__drawScene = drawScene
        self.__token = token
        self.__drawBox=drawBox

        self.__isStartCommand: bool = False

        ##DrawScene
        self.__drawScene.EscOrEnterSignal.connect(self.finishCommand)
        drawScene.ClickedMouse.connect(self.addCoordinate)
        drawScene.MovedMouse.connect(self.mouseMove)
        
        ##ElementDraw
        self.__elementDraw = ElementDraw(self.__drawScene)

        ##Service
        self.__drawService = DrawService(self.__token)

        ##DrawObjs
        self.__drawObjs=DrawObjects(self.__drawScene)

        self.__drawObjs.addLayers(self.__drawService.getLayers(self.__drawBox.id))
        self.__drawObjs.addElements(self.__drawService.getElements(self.__drawBox.id),isService=True)
        self.__drawObjs.addPenStyles(self.__drawService.getPenStyles())

        self.__elementDraw.drawElements(self.__drawObjs.elementObjs)

        ##Snap
        self.__snap = SnapElement(self.__drawScene)
        self.__snapObject = SnapSquare(self.__drawScene)
        self.__drawScene.addItem(self.__snapObject)

        ##Preview
        self.__preview = PreviewObject()
        self.__preview.cancelSignal.connect(self.stopCommand)
        self.__drawScene.addItem(self.__preview)

        self.setRadius()
        self.radius: float = 10


    def mouseMove(self, scenePos):
        self.__preview.setMousePosition(scenePos)
        self.__drawScene.updateScene()
        self.__snap.snapPoints(scenePos)

    def startCommand(self,command: CommandEnums):
        self.__drawService.startCommand(
            command, self.__drawBox.id, self.__selectedLayer.id, self.__selectedPen.id)
        self.__preview.setElementType(command.value)
        self.__isStartCommand = True

    def stopCommand(self):
        self.__drawService.stopCommand()
        self.__isStartCommand=False

    def finishCommand(self):self.addElement(self.__drawService.isFinish())
    
    def addCoordinate(self, coordinate: QPointF):
        if self.__isStartCommand == True:
            if self.__snap.getSnapPoint() != None:
                self.__preview.addPoint(self.__snap.getSnapPoint())
            else:
                element = self.__drawService.addCoordinate(
                    round(coordinate.x(),4), round(coordinate.y(),4)
                )
                self.__preview.addPoint(coordinate)
                self.addElement(element)

    def changeSelectedLayer(self,layerName:str):
        for i in self.__drawObjs.layers:
            if i.name==layerName:
                self.selectedLayer=i

    def removeElement(self,element:ElementObj):self.__drawObjs.removeElement(element)
    def addElement(self,element:Element or None):
        if element !=None:
            self.__drawObjs.addElement(element)
            self.__elementDraw.drawElement(self.__drawObjs.getLastElementObj())
            self.__preview.stop()
            self.__isStartCommand = False
    
    def addLayer(self,layer: Layer):self.__drawObjs.addLayer(layer)
    def removeLayer(self,layer: Layer,deleteElements: bool=True):
        if(deleteElements):
            self.__elementDraw.removeElements(layer.elements)
        self.__drawObjs.removeLayer(layer,deleteElements)

    def updateScene(self):self.__drawScene.updateScene()

    def setRadius(self,radius:float=50):
        self.__drawService.setRadius(radius)
        self.__preview.setRadius(radius)

    def saveDraw(self):
        for i in self.layers:
            print("layer--",i.state)
            print("pen--",i.pen.state)
        
        ## Kaydettikten sonra kaydedilen nesnelerin idlerini kaydetmek gerekiyor
        self.__drawService.saveElements(list(filter(lambda x:x.state==StateTypes.added,self.elements)))

        for i in self.__drawObjs.elementObjs:
            print("element--",i.element.state)



        
