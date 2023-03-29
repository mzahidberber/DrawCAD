from Model.BaseModel import BaseModel
from Model.DrawEnums import CInfo


class Color(BaseModel):
    __colorId: int
    __colorName: str
    __colorRed: int
    __colorBlue: int
    __colorGreen: int

    @property
    def colorId(self):
        return self.__colorId

    @property
    def colorName(self)->str:return self.__colorName
    @colorName.setter
    def colorName(self,name:str):self.__colorName=name

    @property
    def colorRed(self):
        return self.__colorRed

    @colorRed.setter
    def colorRed(self, red: int):
        self.__colorRed = red

    @property
    def colorBlue(self):
        return self.__colorBlue

    @colorBlue.setter
    def colorBlue(self, blue: int):
        self.__colorBlue = blue

    @property
    def colorGreen(self):
        return self.__colorGreen

    @colorGreen.setter
    def colorGreen(self, green: int):
        self.__colorGreen = green

    def __init__(self, colorInformation: dict):
        self.__colorInfo = colorInformation
        self.__colorId = self.__colorInfo[CInfo.colorId.value]
        self.__colorName = self.__colorInfo[CInfo.colorName.value]
        self.__colorRed = self.__colorInfo[CInfo.colorRed.value]
        self.__colorBlue = self.__colorInfo[CInfo.colorBlue.value]
        self.__colorGreen = self.__colorInfo[CInfo.colorGreen.value]

    

    def to_dict(self) -> dict:
        return {
            CInfo.colorId.value: self.__colorId,
            CInfo.colorName.value: self.__colorName,
            CInfo.colorRed.value: self.__colorRed,
            CInfo.colorBlue.value: self.__colorBlue,
            CInfo.colorGreen.value: self.__colorGreen,
        }
