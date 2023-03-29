
from Elements import ElementObj
from Model.BaseModel import BaseModel
from Model.Pen import Pen
from Model.DrawEnums import LInfo


class Layer(BaseModel):
    __layerId: int or None
    __layerName: str
    __layerLock: bool
    __layerVisibility: bool
    __layerThickness: float
    __layerDrawBoxId: int
    __layerPenId: int
    __layerPen: Pen
    __layerElements:list[ElementObj] or None

    @property
    def layerId(self):
        return self.__layerId

    @property
    def layerName(self):
        return self.__layerName
    @layerName.setter
    def layerName(self,name:str):self.__layerName=name

    @property
    def layerLock(self):
        return self.__layerLock
    @layerLock.setter
    def layerLock(self,lock:bool):self.__layerLock=lock

    @property
    def layerVisibility(self):
        return self.__layerVisibility
    @layerVisibility.setter
    def layerVisibility(self,visibility:bool):self.__layerVisibility=visibility

    @property
    def layerThickness(self):
        return self.__layerThickness
    @layerThickness.setter
    def layerThickness(self,thickness:float):self.__layerThickness=thickness

    @property
    def layerDrawBoxId(self):
        return self.__layerDrawBoxId

    @property
    def layerPenId(self):
        return self.__layerPenId

    @property
    def layerPen(self):
        return self.__layerPen

    @property
    def layerElements(self) -> list[ElementObj]:return self.__layerElements
    @layerElements.setter
    def layerElements(self,elements:list[ElementObj]):self.__layerElements=elements

    def __init__(self, layerInfo: dict=None,
                layerId:int=None,layerName: str=None,
                layerLock:bool=False,layerThickness: float=1,
                layerVisibility: bool=True,layerDrawBoxId: int=None,
                layerPen:Pen=None) -> None:
        
        if(layerInfo!=None):
            self.__layerInfo = layerInfo
            self.__layerId = self.__layerInfo[LInfo.layerId.value]
            self.__layerName = self.__layerInfo[LInfo.layerName.value]
            self.__layerLock = self.__layerInfo[LInfo.layerLock.value]
            self.__layerVisibility = self.__layerInfo[LInfo.LayerVisibility.value]
            self.__layerThickness = self.__layerInfo[LInfo.LayerThickness.value]
            self.__layerDrawBoxId = self.__layerInfo[LInfo.DrawBoxId.value]
            self.__layerPenId = self.__layerInfo[LInfo.PenId.value]
            # self.__layerElements=MappingModel.mapDictToClass(self.__layerInfo[LInfo.elements.value],Element)
            self.__layerPen = Pen(self.__layerInfo[LInfo.Pen.value])
        else:
            self.__layerId = layerId
            self.__layerName = layerName
            self.__layerLock = layerLock
            self.__layerVisibility = layerVisibility
            self.__layerThickness = layerThickness
            self.__layerDrawBoxId = layerDrawBoxId
            self.__layerPenId = layerPen.penId
            # self.__layerElements=MappingModel.mapDictToClass(self.__layerInfo[LInfo.elements.value],Element)
            self.__layerPen = layerPen


        self.__layerElements=[]


    def addElement(self,element:ElementObj):self.__layerElements.append(element)

    def copy(self):return Layer(
        layerId=None,layerName=self.layerName,
        layerLock=self.layerLock,layerThickness=self.layerThickness,layerVisibility=self.layerVisibility,
        layerDrawBoxId=self.layerDrawBoxId,layerPen=self.layerPen)

    def lockElements(self):
        for e in self.__layerElements:
            e.elementSelectedOff()

    def unlockElements(self):
        for e in self.__layerElements:
            e.elementSelectedOn()

    def hideElements(self):
        for e in self.__layerElements:
            e.elementHide()

    def showElements(self):
        for e in self.__layerElements:
            e.elementShow()

    def to_dict(self) -> dict:
        return {
            LInfo.layerId.value: self.__layerId,
            LInfo.layerName.value: self.__layerName,
            LInfo.layerLock.value: self.__layerLock,
            LInfo.LayerVisibility.value: self.__layerVisibility,
            LInfo.LayerThickness.value: self.__layerThickness,
            LInfo.DrawBoxId.value: self.__layerDrawBoxId,
            LInfo.PenId.value: self.__layerPenId,
            LInfo.Pen.value: self.__layerPen.to_dict(),
            # LInfo.elements.value:MappingModel.mapClassToDict(self.__layerElements),
        }
