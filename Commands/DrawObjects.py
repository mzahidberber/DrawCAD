from Elements import ElementObj
from Model import Element, Layer,PenStyle,Pen
from Model.DrawEnums import StateTypes
from UI import DrawScene
from Helpers.Select.Select import Select

class DrawObjects:
    __layers:list[Layer]
    __elementObjs:list[ElementObj]
    __elements:list[Element]
    __penStyles:list[PenStyle]
    __drawScene:DrawScene
    __selectedLayer:Layer

    @property
    def layers(self) -> list[Layer]:return self.__layers
    @layers.setter
    def layers(self,layers:list[Layer]):self.__layers=layers

    @property
    def selectedLayer(self) -> Layer:return self.__selectedLayer
    @selectedLayer.setter
    def selectedLayer(self,layer:Layer):self.__selectedLayer=layer


    @property
    def elementObjs(self) -> list[ElementObj]:return self.__elementObjs
    @elementObjs.setter
    def elementObjs(self,elementObjs:list[ElementObj]):self.__elementObjs=elementObjs

    @property
    def elements(self)->list[Element]:return self.__elements

    @property
    def penStyles(self) -> list[PenStyle]:return self.__penStyles

    @property
    def pens(self)->list[Pen]:return list(map(lambda x:x.pen,self.layers))
    

    def __init__(self,commandPanel,drawScene:DrawScene,select:Select) -> None:
        self.__commandPanel=commandPanel
        self.__drawScene=drawScene
        self.__select=select
        self.__layers=[]
        self.__elementObjs=[]
        self.__penStyles=[]
        self.__elements=[]
        
    def addElement(self,element:Element,isService: bool=False)-> ElementObj:

        for layer in self.layers:
            if(element.layerId==layer.id):element.layer=layer
        if isService:element.state = StateTypes.unchanged
        else:element.state = StateTypes.added
        if not hasattr(element,"layer"):element.layer=self.selectedLayer
        self.elements.append(element)
        elementObj=ElementObj(element,self.__drawScene,self.__select)
        elementObj.elementUpdate.connect(self.__commandPanel.updateElement)
        self.__drawScene.addItem(elementObj)
        self.__elementObjs.append(elementObj)
        element.layer.addElement(elementObj)
        return elementObj

    def addElements(self,elements:list[Element],isService: bool=False) -> None:
        if elements is not None:
            for element in elements:self.addElement(element,isService=isService)

    def removeElement(self, elementObj:ElementObj) ->None:
        elementObj.element.layer.elements.remove(elementObj)
        if elementObj.element.id is None:
            self.__elementObjs.remove(elementObj)
        else:
            elementObj.element.state = StateTypes.delete

        self.__drawScene.removeItem(elementObj)

    def getLastElementObj(self)-> ElementObj:return self.elementObjs[-1]

    def addLayers(self,layers: list[Layer])->None:
        if layers is not None:self.__layers.extend(layers)
        else:self.addLayer(Layer.create0Layer())
    
    def addLayer(self,layer:Layer)-> None :self.__layers.append(layer)
    
    def removeLayer(self,layer: Layer,removeElements: bool=True) -> None:
        ##Elementin Layeri degişirse silinmeyecek düzelt
        if removeElements:
            for element in layer.elements:self.removeElement(element)
        if layer.id is not None:
            layer.state=StateTypes.delete
        else:
            self.__layers.remove(layer)
    
    
    
    def addPenStyles(self,penStyles: list[PenStyle])->None:self.__penStyles.extend(penStyles)

    def lockElements(self):[l.lockElements() for l in self.layers]
    def unlockElements(self):[l.unlockElements() for l in self.layers]


