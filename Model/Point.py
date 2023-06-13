from Model.BaseModel import BaseModel
from Model.DrawEnums import PInfo,StateTypes


class Point(BaseModel):
    __X: float
    __Y: float
    __Z: float = 1
    __elementId: int
    __pointTypeId: int


    @property
    def x(self) -> float:
        return self.__X

    @x.setter
    def x(self, point: float) -> None:
        self.__X = point
        self.state=StateTypes.update

    @property
    def y(self) -> float:
        return self.__Y

    @y.setter
    def y(self, point: float) -> None:
        self.__Y = point
        self.state=StateTypes.update

    @property
    def z(self) -> float:
        return self.__Z

    @z.setter
    def z(self, point: float) -> None:
        self.__Z = point
        self.state=StateTypes.update

    @property
    def elementId(self) -> int:
        return self.__elementId

    @property
    def pointTypeId(self) -> int:
        return self.__pointTypeId

    def __init__(self, pInfo: dict=None,id:int=None,x:float=None,y:float=None,elementId:int=None,pointTypeId:int=None) -> None:
        if pInfo is not None:
            self.__pInfo = pInfo
            self._id = self.__pInfo[PInfo.id.value]
            self.__X = self.__pInfo[PInfo.x.value]
            self.__Y = self.__pInfo[PInfo.y.value]
            self.__elementId = self.__pInfo[PInfo.elementId.value]
            self.__pointTypeId = self.__pInfo[PInfo.pointTypeId.value]
        else:
            self._id=id
            self.__X=x
            self.__Y=y
            self.__elementId=elementId
            self.__pointTypeId=pointTypeId

        self.state=StateTypes.unchanged

    def copy(self):return Point(x=self.x,y=self.y,elementId=self.elementId,pointTypeId=self.pointTypeId)

    def to_dict_geo(self) -> dict:
        return {"X": self.__X, "Y": self.__Y, "Z": self.__Z}

    def to_dict(self) -> dict:
        return {
            PInfo.id.value: self._id,
            PInfo.x.value: self.__X,
            PInfo.y.value: self.__Y,
            PInfo.elementId.value: self.__elementId,
            PInfo.pointTypeId.value: self.__pointTypeId,
        }
