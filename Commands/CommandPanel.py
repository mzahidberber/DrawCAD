from PyQt5.QtCore import QPointF
from Elements import ElementObj
from Model import DrawBox, Element, Layer, pen, PenStyle
from Service import DrawService
from Service.Model import Token
from UI import DrawScene
from Commands.CommandEnums import CommandEnums
from Commands.ElementDraw import ElementDraw
from Helpers.Preview import PreviewObject
from Helpers.Snap import SnapElement, SnapSquare
from Model.DrawEnums import StateTypes


class CommandPanel:
    __drawElementObj:list[ElementObj]
    __layers:list[Layer]
    __pens:list[pen]
    __penStyles:list[PenStyle]
    __selectedLayer:Layer
    __selectedPen:pen
    __drawBox=DrawBox

    @property
    def selectedLayer(self)-> Layer:return self.__selectedLayer
    @selectedLayer.setter
    def selectedLayer(self,layer:Layer):self.__selectedLayer=layer

    @property
    def selectedPen(self)-> pen:return self.__selectedPen
    @selectedPen.setter
    def selectedPen(self,pen:pen):self.__selectedPen=pen

    @property
    def drawElementObjects(self):return self.__drawElementObj
    @drawElementObjects.setter
    def drawElementObjects(self,elements:list[ElementObj]):self.__drawElementObj=elements

    @property
    def layers(self):return self.__layers
    @layers.setter
    def layers(self,layers:list[Layer]):self.__layers=layers
    
    @property
    def pens(self):return self.__pens
    @pens.setter
    def pens(self,pens:list[pen]):self.__pens=pens

    @property
    def penStyles(self):return self.__penStyles

    @property
    def drawBox(self)->DrawBox :return self.__drawBox



    def __init__(self, drawScene: DrawScene, token: Token,drawBox:DrawBox) -> None:
        self.__drawScene = drawScene
        self.__token = token
        self.__drawBox=drawBox

        self.__isStartCommand: bool = False

        self.__drawElementObj:list[ElementObj]=[]

        self.__snap: SnapElement = SnapElement(self.__drawScene)
        self.__elementDraw: ElementDraw = ElementDraw(self.__drawScene)
        self.__drawService: DrawService = DrawService.DrawService(self.__token)

        self.__snapObject = SnapSquare(self.__drawScene)
        self.__drawScene.addItem(self.__snapObject)

        self.__preview = PreviewObject()
        self.__drawScene.addItem(self.__preview)

        drawScene.ClickedMouse.connect(self.addCoordinate)
        drawScene.MovedMouse.connect(self.mouseMove)

        
        self.layers = self.__drawService.getLayers(self.__drawBox.id)
        self.elements = self.__drawService.getElements(self.__drawBox.id)
        
        self.__penStyles=self.__drawService.getPenStyles()

        

        for element in self.elements:
            elementObj=ElementObj(element,self.__drawScene)
            for layer in self.layers:
                if layer.id == element.layerId:
                    element.layer = layer
                    element.state=StateTypes.unchanged
                    layer.addElement(elementObj)

            self.__drawElementObj.append(self.__elementDraw.drawElement(elementObj))

        

        self.radius: float = 10

    def mouseMove(self, scenePos):
        self.__preview.setMousePosition(scenePos)
        self.__drawScene.updateScene()
        self.__snap.snapPoints(scenePos)

    def startCommand(self,command: CommandEnums):
        self.__drawService.startCommand(
            command, self.__drawBox.id, self.__selectedLayer.id, self.__selectedPen.id
        )
        self.__preview.setElementType(command.value)
        self.__isStartCommand = True

    def addCoordinate(self, coordinate: QPointF):
        # print(coordinate)
        if self.__isStartCommand == True:
            if self.__snap.getSnapPoint() != None:
                self.__preview.addPoint(self.__snap.getSnapPoint())
            else:
                element = self.__drawService.addCoordinate(
                    coordinate.x(), coordinate.y()
                )
                self.__preview.addPoint(coordinate)
                if element != None:
                    for i in self.layers:
                        if element.layerId == i.id:
                            element.layer = i
                            
                    
                    self.__elementDraw.drawElement(ElementObj(element,self.__drawScene))
                    self.__preview.stop()
                    self.__isStartCommand = False
                    element.state=StateTypes.added
                    self.elements.append(element)

    def changeSelectedLayer(self,layerName: str):
        for i in self.layers:
            if i.name==layerName:
                self.selectedLayer=i

    def removeElement(self,element:ElementObj):
        #Burayı yaz
        self.__drawElementObj.remove()
        self.elements.remove(element)


    def addLayer(self,layer: Layer):self.layers.append(layer)

    def removeLayer(self,layer: Layer):self.layers.remove(layer)

    def updateScene(self):self.__drawScene.updateScene()

    def saveDraw(self):
        for i in self.layers:
            print("layer--",i.state)
            print("pen--",i.pen.state)
        
        ## Kaydettikten sonra kaydedilen nesnelerin idlerini kaydetmek gerekiyor
        self.__drawService.saveElements(list(filter(lambda x:x.state==StateTypes.added,self.elements)))

        for i in self.elements:
            print("element--",i.state)



        
