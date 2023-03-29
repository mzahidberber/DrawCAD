from Model.BaseModel import BaseModel
from Model.DrawEnums import PSInfo


class PenStyle(BaseModel):
    __penStyleId: int
    __penStyleName: str

    @property
    def penStyleId(self):
        return self.__penStyleId
    

    @property
    def penStyleName(self):
        return self.__penStyleName

    @penStyleName.setter
    def penStyleName(self, name: str):
        self.__penStyleName = name

    def __init__(self, penStyleInformation: dict):
        self.__penStyleInfo = penStyleInformation
        self.__penStyleId = self.__penStyleInfo[PSInfo.penStyleId.value]
        self.__penStyleName = self.__penStyleInfo[PSInfo.penStyleName.value]

    def to_dict(self) -> dict:
        return {
            PSInfo.penStyleId.value: self.__penStyleId,
            PSInfo.penStyleName.value: self.__penStyleName,
        }
