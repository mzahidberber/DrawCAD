from Model.BaseModel import BaseModel
from Model.Pen import Pen
from Model.DrawEnums import LInfo,StateTypes
from Model.MappingModel import MappingModel
from Model.Element import Element


class Layer(BaseModel):
    __name: str
    __lock: bool
    __visibility: bool
    __thickness: float
    __drawBoxId: int
    __penId: int
    __pen: Pen
    __elements:list[Element] or None
    


    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self,name:str):
        if self.state != StateTypes.added:
            self.state = StateTypes.update
        self.__name=name

    @property
    def lock(self):
        return self.__lock
    @lock.setter
    def lock(self,lock:bool):
        if self.state != StateTypes.added:
            self.state = StateTypes.update
        self.__lock=lock

    @property
    def visibility(self):
        return self.__visibility
    @visibility.setter
    def visibility(self,visibility:bool):
        if self.state != StateTypes.added:
            self.state = StateTypes.update
        self.__visibility=visibility

    @property
    def thickness(self):
        return self.__thickness
    @thickness.setter
    def thickness(self,thickness:float):
        if self.state != StateTypes.added:
            self.state = StateTypes.update
        self.__thickness=thickness

    @property
    def drawBoxId(self):
        return self.__drawBoxId
    @drawBoxId.setter
    def drawBoxId(self,id:int):self.__drawBoxId=id

    @property
    def penId(self):
        return self.__penId

    @penId.setter
    def penId(self,id:int):self.__penId=id

    @property
    def pen(self):
        return self.__pen
    @pen.setter
    def pen(self,pen:Pen):self.__pen=pen

    @property
    def elements(self) -> list[Element]:return self.__elements
    @elements.setter
    def elements(self,elements:list[Element]):
        if self.state!=StateTypes.added:
            self.state=StateTypes.update
        self.__elements=elements

    

    def __init__(self, layerInfo: dict=None,
                id:int=0,name: str=None,
                lock:bool=True,thickness: float=1,
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
            self.__pen = Pen(self.__layerInfo[LInfo.pen.value])

            if self.__layerInfo[LInfo.elements.value] is not None:
                self.elements=list(map(lambda x:Element(x),self.__layerInfo[LInfo.elements.value]))
                for e in self.elements:e.layerName=self.name

                if self.id != 0:
                    self.state = StateTypes.unchanged
                else:
                    self.state = StateTypes.added
            else:
                self.__elements = []

        else:
            self._id = id
            self.__name = name
            self.__lock = lock
            self.__visibility = visibility
            self.__thickness = thickness
            self.__drawBoxId = drawBoxId
            self.__penId = pen.id
            self.__pen = pen

            self.__elements = []

            self.state = StateTypes.added





    def addElement(self,element:Element):self.__elements.append(element)

    def copy(self):return Layer(
        id=0,name=self.name,
        lock=self.lock,thickness=self.thickness,visibility=self.visibility,
        drawBoxId=self.drawBoxId,pen=self.pen.copy())



    @staticmethod
    def create0Layer(drawBoxId:int):
        pen=Pen(penStyleId=1,red=150,blue=150,green=150)
        pen.state=StateTypes.added
        return Layer(name="0",pen=pen,drawBoxId=drawBoxId)


    def to_dict_save(self):
        return {
            LInfo.id.value: self._id,
            LInfo.lname.value: self.__name,
            LInfo.lock.value: self.__lock,
            LInfo.visibility.value: self.__visibility,
            LInfo.thickness.value: self.__thickness,
            LInfo.drawBoxId.value: self.__drawBoxId,
            LInfo.penId.value: self.__penId,
            LInfo.pen.value:self.pen.to_dict_save(),
            LInfo.elements.value:MappingModel.mapClassToDictSave(list(map(lambda x:x,self.elements)))
            # LInfo.pen.value: self.__pen.to_dict(),
            # LInfo.elements.value:MappingModel.mapClassToDict(self.__layerElements),
        }

    def to_dict(self) -> dict:
        return {
            LInfo.id.value: self._id,
            LInfo.lname.value: self.__name,
            LInfo.lock.value: self.__lock,
            LInfo.visibility.value: self.__visibility,
            LInfo.thickness.value: self.__thickness,
            LInfo.drawBoxId.value: self.__drawBoxId,
            LInfo.penId.value: self.__penId,
            # LInfo.pen.value: self.__pen.to_dict(),
            # LInfo.elements.value:MappingModel.mapClassToDict(self.__layerElements),
        }
