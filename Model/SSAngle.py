from Model.BaseModel import BaseModel
from Model.DrawEnums import SSAInfo,StateTypes


class SSAngle(BaseModel):
    __type: str
    __value: float
    __elementId: int


    @property
    def type(self) -> int:
        return self.__type

    @property
    def value(self) -> int:
        return self.__value
    @value.setter
    def value(self,value: float):
        self.__value=value
        self.state=StateTypes.update

    @property
    def elementId(self) -> int:
        return self.__elementId

    def __init__(self, ssangleInfo: dict) -> None:
        self.__ssangeInfo = ssangleInfo
        self._id = self.__ssangeInfo[SSAInfo.id.value]
        self.__type = self.__ssangeInfo[SSAInfo.type.value]
        self.__value = self.__ssangeInfo[SSAInfo.value.value]
        self.__elementId = self.__ssangeInfo[SSAInfo.elementId.value]

        self.state=StateTypes.unchanged

    def to_dict(self) -> dict:
        return {
            SSAInfo.id.value: self._id,
            SSAInfo.type.value: self.__type,
            SSAInfo.value.value: self.__value,
            SSAInfo.elementId.value: self.__elementId,
        }
