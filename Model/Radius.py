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

    def __init__(self, radiusInfo: dict) -> None:
        self.__radiusInfo = radiusInfo
        self._id = self.__radiusInfo[RInfo.id.value]
        self.__value = self.__radiusInfo[RInfo.rvalue.value]
        self.__elementId = self.__radiusInfo[RInfo.elementId.value]

        self.state=StateTypes.unchanged

    def to_dict(self) -> dict:
        return {
            RInfo.id.value: self._id,
            RInfo.rvalue.value: self.__value,
            RInfo.elementId.value: self.__elementId,
        }
