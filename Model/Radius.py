from Model.BaseModel import BaseModel
from Model.DrawEnums import RInfo,StateTypes


class Radius(BaseModel):
    __value: float
    __elementId: int


    @property
    def value(self) -> float:
        return self.__value

    @value.setter
    def value(self, radius: float):
        self.__value = radius
        self.state=StateTypes.update

    @property
    def elementId(self) -> int:
        return self.__elementId

    def __init__(self, radiusInfo: dict=None,id:int=0,value:float=None,elementId:int=None) -> None:
        self.__radiusInfo = radiusInfo
        if self.__radiusInfo is not None:
            self._id = self.__radiusInfo[RInfo.id.value]
            self.__value = self.__radiusInfo[RInfo.rvalue.value]
            self.__elementId = self.__radiusInfo[RInfo.elementId.value]
        else:
            self._id=id
            self.__value=value
            self.__elementId=elementId

        if self.id != 0:
            self.state = StateTypes.unchanged
        else:
            self.state = StateTypes.added

    def copy(self): return Radius(value=self.value,elementId=self.elementId)

    def to_dict_save(self) -> dict:
        return {
            RInfo.id.value: self._id,
            RInfo.rvalue.value: self.__value,
            RInfo.elementId.value: self.__elementId,
        }

    def to_dict(self) -> dict:
        return {
            RInfo.id.value: self._id,
            RInfo.rvalue.value: self.__value,
            RInfo.elementId.value: self.__elementId,
        }
