
from Elements import ElementObj
from Model.BaseModel import BaseModel
from Model.Pen import Pen
from Model.DrawEnums import LInfo,StateTypes



class Layer(BaseModel):
    __name: str
    __lock: bool
    __visibility: bool
    __thickness: float
    __drawBoxId: int
    __penId: int
    __pen: Pen
    __elements:list[ElementObj] or None
    


    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self,name:str):
        self.state=StateTypes.update
        self.__name=name

    @property
    def lock(self):
        return self.__lock
    @lock.setter
    def lock(self,lock:bool):
        self.state=StateTypes.update
        self.__lock=lock

    @property
    def visibility(self):
        return self.__visibility
    @visibility.setter
    def visibility(self,visibility:bool):
        self.state=StateTypes.update
        self.__visibility=visibility

    @property
    def thickness(self):
        return self.__thickness
    @thickness.setter
    def thickness(self,thickness:float):
        self.state=StateTypes.update
        self.__thickness=thickness

    @property
    def drawBoxId(self):
        return self.__drawBoxId

    @property
    def penId(self):
        return self.__penId

    @property
    def pen(self):
        return self.__pen

    @property
    def elements(self) -> list[ElementObj]:return self.__elements
    @elements.setter
    def elements(self,elements:list[ElementObj]):
        self.state=StateTypes.update
        self.__elements=elements

    

    def __init__(self, layerInfo: dict=None,
                id:int=None,name: str=None,
                lock:bool=False,thickness: float=1,
                visibility: bool=True,drawBoxId: int=None,
                pen:Pen=None) -> None:
        
        if(layerInfo!=None):
            self.__layerInfo = layerInfo
            self._id = self.__layerInfo[LInfo.id.value]
            self.__name = self.__layerInfo[LInfo.lname.value]
            self.__lock = self.__layerInfo[LInfo.lock.value]
            self.__visibility = self.__layerInfo[LInfo.visibility.value]
            self.__thickness = self.__layerInfo[LInfo.thickness.value]
            self.__drawBoxId = self.__layerInfo[LInfo.drawBoxId.value]
            self.__penId = self.__layerInfo[LInfo.penId.value]
            # self.__layerElements=MappingModel.mapDictToClass(self.__layerInfo[LInfo.elements.value],Element)
            self.__pen = Pen(self.__layerInfo[LInfo.pen.value])

        else:
            self._id = id
            self.__name = name
            self.__lock = lock
            self.__visibility = visibility
            self.__thickness = thickness
            self.__drawBoxId = drawBoxId
            self.__penId = pen.id
            # self.__layerElements=MappingModel.mapDictToClass(self.__layerInfo[LInfo.elements.value],Element)
            self.__pen = pen



        self.state=StateTypes.unchanged
        self.__elements=[]

    


    def addElement(self,element:ElementObj):self.__elements.append(element)

    def copy(self):return Layer(
        id=None,name=self.name,
        lock=self.lock,thickness=self.thickness,visibility=self.visibility,
        drawBoxId=self.drawBoxId,pen=self.pen)

    def lockElements(self):
        for e in self.__elements:
            e.elementSelectedOff()

    def unlockElements(self):
        for e in self.__elements:
            e.elementSelectedOn()

    def hideElements(self):
        for e in self.__elements:
            e.elementHide()

    def showElements(self):
        for e in self.__elements:
            e.elementShow()

    def to_dict(self) -> dict:
        return {
            LInfo.id.value: self._id,
            LInfo.lname.value: self.__name,
            LInfo.lock.value: self.__lock,
            LInfo.visibility.value: self.__visibility,
            LInfo.thickness.value: self.__thickness,
            LInfo.drawBoxId.value: self.__drawBoxId,
            LInfo.penId.value: self.__penId,
            LInfo.pen.value: self.__pen.to_dict(),
            # LInfo.elements.value:MappingModel.mapClassToDict(self.__layerElements),
        }
