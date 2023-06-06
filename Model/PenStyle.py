from Model.BaseModel import BaseModel
from Model.DrawEnums import PSInfo


class PenStyle(BaseModel):
    __name: str
    

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: str):
        self.__name = name

    def __init__(self, penStyleInformation: dict=None,id:int=None,name:str=None):
        self.__penStyleInfo = penStyleInformation
        if self.__penStyleInfo is not None:
            self._id = self.__penStyleInfo[PSInfo.id.value]
            self.__name = self.__penStyleInfo[PSInfo.psname.value]
        else:
            self._id=id
            self.__name=name

    def to_dict(self) -> dict:
        return {
            PSInfo.id.value: self._id,
            PSInfo.psname.value: self.__name,
        }
