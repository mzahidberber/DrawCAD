from Model.BaseModel import BaseModel
from Model.DrawEnums import SSAInfo,StateTypes


class SSAngle(BaseModel):
    __type: str
    __value: float
    __elementId: int


    @property
    def type(self) -> str:
        return self.__type

    @property
    def value(self) -> float:
        return self.__value
    @value.setter
    def value(self,value: float):
        self.__value=value
        self.state=StateTypes.update

    @property
    def elementId(self) -> int:
        return self.__elementId

    def __init__(self, ssangleInfo: dict=None,id:int=0,type:str=None,value:float=None,elementId:int=None) -> None:
        self.__ssangeInfo = ssangleInfo
        if self.__ssangeInfo is not None:
            self._id = self.__ssangeInfo[SSAInfo.id.value]
            self.__type = self.__ssangeInfo[SSAInfo.type.value]
            self.__value = self.__ssangeInfo[SSAInfo.ssvalue.value]
            self.__elementId = self.__ssangeInfo[SSAInfo.elementId.value]
        else:
            self._id=id
            self.__type=type
            self.__value=value
            self.__elementId=elementId

        if self.id != 0:
            self.state = StateTypes.unchanged
        else:
            self.state = StateTypes.added

    def copy(self) : return SSAngle(type=self.type,value=self.value,elementId=self.elementId)

    def to_dict_save(self) -> dict:
        return {
            SSAInfo.id.value: self._id,
            SSAInfo.type.value: self.__type,
            SSAInfo.ssvalue.value: self.__value,
            SSAInfo.elementId.value: self.__elementId,
        }

    def to_dict(self) -> dict:
        return {
            SSAInfo.id.value: self._id,
            SSAInfo.type.value: self.__type,
            SSAInfo.ssvalue.value: self.__value,
            SSAInfo.elementId.value: self.__elementId,
        }
