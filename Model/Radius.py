from Model.BaseModel import BaseModel
from Model.DrawEnums import RInfo
class Radius(BaseModel):
    __radiusId:int
    __radiusValue:float
    __radiusElementId:int

    @property
    def radiusId(self) -> int:return self.__radiusId

    @property
    def radiusValue(self) -> float:return self.__radiusValue
    @radiusValue.setter
    def radiusValue(self,radius:float):self.__radiusValue=radius

    @property
    def radiusElementId(self) -> int:return self.__radiusElementId

    def __init__(self,radiusInfo:dict) -> None:
        self.__radiusInfo=radiusInfo
        self.__radiusId=self.__radiusInfo[RInfo.radiusId.value]
        self.__radiusValue=self.__radiusInfo[RInfo.radiusValue.value]
        self.__radiusElementId=self.__radiusInfo[RInfo.radiusElementId.value]

    def to_dict(self) -> dict:
        return {
            RInfo.radiusId.value:self.__radiusId,
            RInfo.radiusValue.value:self.__radiusValue,
            RInfo.radiusElementId.value:self.__radiusElementId
            }