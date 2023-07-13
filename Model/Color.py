from Model.BaseModel import BaseModel
from Model.DrawEnums import CInfo


class Color(BaseModel):
    __name: str
    __red: int
    __blue: int
    __green: int


    @property
    def name(self)->str:return self.__name
    @name.setter
    def name(self,name:str):self.__name=name

    @property
    def red(self):
        return self.__red

    @red.setter
    def red(self, red: int):
        self.__red = red

    @property
    def blue(self):
        return self.__blue

    @blue.setter
    def blue(self, blue: int):
        self.__blue = blue

    @property
    def green(self):
        return self.__green

    @green.setter
    def green(self, green: int):
        self.__green = green

    def __init__(self, colorInformation: dict):
        self.__colorInfo = colorInformation
        self._id = self.__colorInfo[CInfo.id.value]
        self.__name = self.__colorInfo[CInfo.cname.value]
        self.__red = self.__colorInfo[CInfo.red.value]
        self.__blue = self.__colorInfo[CInfo.blue.value]
        self.__green = self.__colorInfo[CInfo.green.value]

    

    def to_dict(self) -> dict:
        return {
            CInfo.id.value: self._id,
            CInfo.cname.value: self.__name,
            CInfo.red.value: self.__red,
            CInfo.blue.value: self.__blue,
            CInfo.green.value: self.__green,
        }

    def to_dict_save(self) -> dict:
        return {
            CInfo.id.value: self._id,
            CInfo.cname.value: self.__name,
            CInfo.red.value: self.__red,
            CInfo.blue.value: self.__blue,
            CInfo.green.value: self.__green,
        }
