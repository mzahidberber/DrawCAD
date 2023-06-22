from Elements import ElementObj
from Model import Element, Layer,PenStyle,Pen,DrawBox
from Model.DrawEnums import StateTypes
from UI import DrawScene
from Helpers.Select.Select import Select
from CrossCuttingConcers.Handling.ErrorHandle import ErrorHandle


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
            if element.layerId != 0:
                if element.layerId==layer.id:
                    element.layer=layer
                    element.layerName=layer.name
            else:
                if element.layerName==layer.name:
                    element.layer=layer
        if isService:element.state = StateTypes.unchanged
        else:element.state = StateTypes.added
        if not hasattr(element,"layer"):element.layer=self.__commandPanel.selectedLayer
        self.elements.append(element)
        elementObj=ElementObj(element,self.__drawScene,self.__select)
        elementObj.elementUpdate.connect(self.__commandPanel.updateElement)
        self.__drawScene.addItem(elementObj)
        self.__elementObjs.append(elementObj)
        element.layer.addElement(element)
        return elementObj

    def addElements(self,elements:list[Element],isService: bool=False) -> None:
        if elements is not None:
            for element in elements:self.addElement(element,isService=isService)


    def addElementObjs(self,elements:list[Element],isService: bool=False) -> None:
        if elements is not None:
            for element in elements:self.addElementObj(element,isService=isService)

    def addElementObj(self,element:Element,isService: bool=False)-> ElementObj:
        for layer in self.layers:
            if element.layerId != 0:
                if element.layerId==layer.id:
                    element.layer=layer
                    element.layerName=layer.name
            else:
                if element.layerName==layer.name:
                    element.layer=layer
                    element.layerName = layer.name
        if isService:element.state = StateTypes.unchanged
        else:element.state = StateTypes.added
        if not hasattr(element,"layer"):element.layer=self.__commandPanel.selectedLayer
        elementObj=ElementObj(element,self.__drawScene,self.__select)
        elementObj.elementUpdate.connect(self.__commandPanel.updateElement)
        self.__drawScene.addItem(elementObj)
        self.__elementObjs.append(elementObj)
        return elementObj

    def changeElement(self,oldElement:Element,newElement:Element):
        self.elementObjs[self.elements.index(oldElement)].element=newElement
        self.elements[self.elements.index(oldElement)]=newElement

    def synchronousLists(self):
        self.__elements.clear()
        [self.__elements.append(e.element) for e in self.elementObjs]
    def removeElement(self, element:Element, deleteId:bool=False):
        eObj=next(e for e in self.elementObjs if e.element==element)
        element.layer.elements.remove(element)
        if element.id != 0 and not deleteId:
            element.state = StateTypes.delete
        else:
            self.__elementObjs.remove(eObj)

        self.synchronousLists()
        self.__drawScene.removeItem(eObj)

    def removeElements(self,elements:list[Element], deleteId:bool=False):
        for element in elements:
            eObj=next(e for e in self.elementObjs if e.element==element)
            element.layer.elements.remove(element)
            if element.id != 0 and not deleteId:
                element.state = StateTypes.delete
            else:
                self.__elementObjs.remove(eObj)

            self.__drawScene.removeItem(eObj)
        self.synchronousLists()

    def removeElementObj(self, elementObj:ElementObj, deleteId:bool=False) ->None:
        elementObj.element.layer.elements.remove(elementObj.element)
        if elementObj.element.id != 0 and not deleteId:
            elementObj.element.state = StateTypes.delete
        else:
            self.__elementObjs.remove(elementObj)

        self.synchronousLists()
        self.__drawScene.removeItem(elementObj)

    def removeElementObjs(self, elementObjs:list[ElementObj], deleteId:bool=False) ->None:
        for elementObj in elementObjs:
            elementObj.element.layer.elements.remove(elementObj)
            if elementObj.element.id != 0 and not deleteId:
                elementObj.element.state = StateTypes.delete
            else:
                self.__elementObjs.remove(elementObj)
            self.__drawScene.removeItem(elementObj)

        self.synchronousLists()


    def getLastElementObj(self)-> ElementObj:return self.elementObjs[-1]


    def addLayers(self, layers: list[Layer], penStateAdd:bool=False,addElement:bool=False)->None:
        penState=list(map(lambda x:x.pen.state,layers))
        if layers is not None:
            for i in layers:
                if penStateAdd:i.pen.state=StateTypes.added
                self.addLayer(i,penStateAdd=penStateAdd)
        else:
            self.addLayer(Layer.create0Layer(self.__commandPanel.drawBox.id))
        if len(self.__commandPanel.drawBox.layers)==0:
            self.__commandPanel.drawBox.layers.extend(self.layers)
        if addElement:
            addElement=False
            if layers[0].state==StateTypes.unchanged:addElement=True
            [self.addElementObjs(l.elements,isService=addElement) for l in layers if len(l.elements)!=0]
            list(map(lambda x:self.elements.extend(x.elements),layers))
        for i in layers:i.pen.state=penState[layers.index(i)]

    
    def addLayer(self,layer:Layer, penStateAdd:bool=False)-> None :
        if penStateAdd: layer.pen.state = StateTypes.added
        self.__layers.append(layer)



    
    def removeLayer(self,layer: Layer,removeElements: bool=True) -> None:
        ##Elementin Layeri degişirse silinmeyecek düzelt
        if removeElements:
            for element in layer.elements:self.removeElement(element)
        if layer.id != 0:
            layer.state=StateTypes.delete
        else:
            self.__layers.remove(layer)


    
    
    
    def addPenStyles(self,penStyles: list[PenStyle])->None:self.__penStyles.extend(penStyles)

    def lockElements(self):[l.elementSelectedOff() for l in self.elementObjs]
    def unlockElements(self):[l.elementSelectedOn() for l in self.elementObjs]


