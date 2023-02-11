from Model.BaseModel import BaseModel
from Model.DrawEnums import PInfo
class Point(BaseModel):
    __pointId:int
    __X:float
    __Y:float
    __Z:float=1
    __elementId:int
    __pointTypeId:int

    @property
    def pointId(self) -> int:return self.__pointId
    
    @property
    def pointX(self) -> float:return self.__X
    @pointX.setter
    def pointX(self,point:float) -> None:self.__X=point
    
    @property
    def pointY(self) -> float:return self.__Y
    @pointY.setter
    def pointY(self,point:float) -> None:self.__Y=point

    @property
    def pointZ(self) -> float:return self.__Z
    @pointZ.setter
    def pointZ(self,point:float) -> None:self.__Z=point
    
    @property
    def elementId(self) -> int:return self.__elementId
    
    @property
    def pointTypeId(self) -> int:return self.__pointTypeId

    def __init__(self,pInfo:dict) -> None:
        self.__pInfo=pInfo
        self.__pointId=self.__pInfo[PInfo.pointId.value]
        self.__X=self.__pInfo[PInfo.pointX.value]
        self.__Y=self.__pInfo[PInfo.pointY.value]
        self.__elementId=self.__pInfo[PInfo.elementId.value]
        self.__pointTypeId=self.__pInfo[PInfo.pointTypeId.value]


    def to_dict_geo(self) -> dict:
        return{
            "X":self.__X,
            "Y":self.__Y,
            "Z":self.__Z
        }

    def to_dict(self) -> dict:
        return {
            PInfo.pointId.value:self.__pointId,
            PInfo.pointX.value:self.__X,
            PInfo.pointY.value:self.__Y,
            PInfo.elementId.value:self.__elementId,
            PInfo.pointTypeId.value:self.__pointTypeId
        }



