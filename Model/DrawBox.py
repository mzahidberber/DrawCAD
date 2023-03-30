from Model.Layer import Layer
from Model.BaseModel import BaseModel
from Model.MappingModel import MappingModel
from Model.DrawEnums import DBInfo,StateTypes


class DrawBox(BaseModel):
    __drawBoxId: int
    __drawName: str
    __userId: str
    __layers: list[Layer] or None

    @property
    def drawBoxId(self):
        return self.__drawBoxId

    @property
    def drawName(self):
        return self.__drawName
    @drawName.setter
    def drawName(self,name:str):
        self.state=StateTypes.update
        self.__drawName=name

    @property
    def userId(self):
        return self.__userId

    @property
    def layers(self):
        return self.__layers

    def __init__(self, drawBoxInfo: dict) -> None:
        self.__drawBoxInfo = drawBoxInfo
        self.__drawBoxId = self.__drawBoxInfo[DBInfo.drawBoxId.value]
        self.__drawName = self.__drawBoxInfo[DBInfo.drawName.value]
        self.__userId = self.__drawBoxInfo[DBInfo.userId.value]
        # self.__layers = MappingModel.mapDictToClass(
        #     self.__drawBoxInfo[DBInfo.layers.value], Layer
        # )


        self.state=StateTypes.unchanged

    def to_dict(self) -> dict:
        return {
            DBInfo.drawBoxId.value: self.__drawBoxId,
            DBInfo.drawName.value: self.__drawName,
            DBInfo.userId.value: self.__userId,
            DBInfo.layers.value: MappingModel.mapClassToDict(self.__layers),
        }
