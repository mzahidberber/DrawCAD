from PyQt5.QtCore import QPointF,pyqtSignal,QObject
from Elements import ElementObj
from Model import DrawBox, Element, Layer, Pen, PenStyle
from Service.DrawService import DrawService
from Service.Model import Token
from UI import DrawScene
from Commands.CommandEnums import CommandEnums
from Commands.ElementDraw import ElementDraw
from Commands.DrawObjects import DrawObjects
from Helpers.Preview import PreviewObject
from Helpers.Snap import Snap
from Model.DrawEnums import StateTypes


class CommandPanel(QObject):

    stopCommandSignal=pyqtSignal(bool)
    saveDrawSignal=pyqtSignal(bool)

    __selectedLayer:Layer
    __selectedPen:Pen
    __drawBox=DrawBox
    __drawObjs:DrawObjects
    __drawScene:DrawScene
    __elementDraw:ElementDraw
    __drawService:DrawService
    __snap:Snap
    __preview:PreviewObject

    @property
    def selectedLayer(self)-> Layer:return self.__selectedLayer
    @selectedLayer.setter
    def selectedLayer(self,layer:Layer):
        self.__drawObjs.selectedLayer=layer
        self.__selectedLayer=layer

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



    def __init__(self, drawScene: DrawScene, token: Token, drawBox:DrawBox) -> None:
        super().__init__()
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

        if len(drawBox.layers)==0:
            layers=self.__drawService.getLayers(self.__drawBox.id)
            if len(layers)!=0 and layers!=None:self.__drawObjs.addLayers(layers)
            else:self.__drawObjs.addLayer(Layer.create0Layer())
        else:
            self.__drawObjs.addLayers(drawBox.layers)

        self.__drawObjs.addElements(self.__drawService.getElements(self.__drawBox.id),isService=True)
        self.__drawObjs.addPenStyles(self.__drawService.getPenStyles())

        self.__elementDraw.drawElements(self.__drawObjs.elementObjs)



        ##Preview
        self.__preview = PreviewObject()
        self.__preview.cancelSignal.connect(self.stopCommand)
        self.__drawScene.addItem(self.__preview)

        self.setRadius()
        self.radius: float = 10

        self.selectedLayer=self.__drawObjs.layers[0]

        self.__snap=self.__drawScene.snap


    def mouseMove(self, scenePos):
        if self.__snap.snapPoint is not None:
            self.__preview.setMousePosition(self.__snap.snapPoint)
        else:
            self.__preview.setMousePosition(scenePos)
        self.__drawScene.updateScene()

    def startCommand(self,command: CommandEnums):
        self.__drawService.startCommand(
            command, self.__drawBox.id, self.__selectedLayer.id, self.__selectedPen.id)
        self.__preview.setElementType(command.value)
        self.__isStartCommand = True

    def stopCommand(self):
        self.__drawService.stopCommand()
        self.__isStartCommand=False
        self.stopCommandSignal.emit(False)
        self.__snap.clickPoint = None
        self.__preview.stop()
    def finishCommand(self):
        self.addElement(self.__drawService.isFinish())
    
    def addCoordinate(self, coordinate: QPointF):
        if self.__isStartCommand == True:

            if self.__snap.snapPoint is not None:
                self.__snap.clickPoint = self.__snap.snapPoint
                element = self.__drawService.addCoordinate(
                    round(self.__snap.snapPoint.x(), 4), round(self.__snap.snapPoint.y(), 4)
                )
                self.__preview.addPoint(self.__snap.snapPoint)
                self.addElement(element)
            else:
                self.__snap.clickPoint=coordinate
                element = self.__drawService.addCoordinate(
                    round(coordinate.x(),4), round(coordinate.y(),4)
                )
                self.__preview.addPoint(coordinate)
                self.addElement(element)


    def changeSelectedLayer(self,layerName:str):
        for i in self.__drawObjs.layers:
            if i.name==layerName:
                self.selectedLayer=i

    def removeElement(self,element:ElementObj):
        self.__drawObjs.removeElement(element)
        self.saveDrawSignal.emit(False)
    def addElement(self,element:Element or None):
        if element !=None:
            self.__drawObjs.addElement(element)
            self.__elementDraw.drawElement(self.__drawObjs.getLastElementObj())
            self.__preview.stop()
            self.__isStartCommand = False
            self.saveDrawSignal.emit(False)
            self.stopCommandSignal.emit(False)
            self.__snap.clickPoint=None
    def addLayer(self,layer: Layer):
        self.__drawObjs.addLayer(layer)
        self.saveDrawSignal.emit(False)

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

        self.__drawService.saveElements(list(filter(lambda x:x.state==StateTypes.added,self.__drawObjs.elements)))

        for element in list(filter(lambda x:x.state==StateTypes.added,self.__drawObjs.elements)):
            element.state=StateTypes.unchanged

        for i in self.__drawObjs.elementObjs:
            print("element--",i.element.state)
            self.__drawService.updatePoints(list(filter(lambda x: x.state == StateTypes.update,i.element.points)))
            for i in i.element.points:
                print("points--",i.state)


        self.saveDrawSignal.emit(True)




        
