from Model.BaseModel import BaseModel
from Model.DrawEnums import SSAInfo


class SSAngle(BaseModel):
    __ssAngleId: int
    __ssAngleType: str
    __ssAngleValue: float
    __ssAngleElementId: int

    @property
    def ssAngleId(self) -> int:
        return self.__ssAngleId

    @property
    def ssAngleType(self) -> int:
        return self.__ssAngleType

    @property
    def ssAngleValue(self) -> int:
        return self.__ssAngleValue

    @property
    def ssAngleElementId(self) -> int:
        return self.__ssAngleElementId

    def __init__(self, ssangleInfo: dict) -> None:
        self.__ssangeInfo = ssangleInfo
        self.__ssAngleId = self.__ssangeInfo[SSAInfo.ssangleId.value]
        self.__ssAngleType = self.__ssangeInfo[SSAInfo.ssangleType.value]
        self.__ssAngleValue = self.__ssangeInfo[SSAInfo.ssangleValue.value]
        self.__ssAngleElementId = self.__ssangeInfo[SSAInfo.ssangleElementId.value]

    def to_dict(self) -> dict:
        return {
            SSAInfo.ssangleId.value: self.__ssAngleId,
            SSAInfo.ssangleType.value: self.__ssAngleType,
            SSAInfo.ssangleValue.value: self.__ssAngleValue,
            SSAInfo.ssangleElementId.value: self.__ssAngleElementId,
        }
