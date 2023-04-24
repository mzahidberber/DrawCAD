from Model.Layer import Layer
from Model.BaseModel import BaseModel
from Model.MappingModel import MappingModel
from Model.DrawEnums import DBInfo,StateTypes


class DrawBox(BaseModel):
    __name: str
    __userId: str
    __layers: list[Layer] or None


    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self,name:str):
        self.state=StateTypes.update
        self.__name=name

    @property
    def userId(self):
        return self.__userId

    @property
    def layers(self):
        return self.__layers

    def __init__(self, drawBoxInfo: dict) -> None:
        self.__drawBoxInfo = drawBoxInfo
        self._id = self.__drawBoxInfo[DBInfo.id.value]
        self.__name = self.__drawBoxInfo[DBInfo.dname.value]
        self.__userId = self.__drawBoxInfo[DBInfo.userId.value]
        # self.__layers = MappingModel.mapDictToClass(
        #     self.__drawBoxInfo[DBInfo.layers.value], Layer
        # )


        self.state=StateTypes.unchanged

    def to_dict(self) -> dict:
        return {
            DBInfo.id.value: self._id,
            DBInfo.dname.value: self.__name,
            DBInfo.userId.value: self.__userId,
            DBInfo.layers.value: MappingModel.mapClassToDict(self.__layers),
        }
