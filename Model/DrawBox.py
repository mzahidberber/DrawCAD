import pytz
from Model.Pen import Pen
from Model.Layer import Layer
from Model.BaseModel import BaseModel
from Model.MappingModel import MappingModel
from Model.DrawEnums import DBInfo,StateTypes
from datetime import datetime, timezone, timedelta
import arrow
class DrawBox(BaseModel):
    __name: str
    __userId: str
    __layers: list[Layer]=[]
    __createTime:datetime
    __editTime:datetime
    __isStart:bool=False

    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self,name:str):
        self.state=StateTypes.update
        self.__editTime=datetime.now().replace(tzinfo=timezone(offset=timedelta()))
        self.__name=name

    @property
    def userId(self):
        return self.__userId

    @property
    def layers(self):return self.__layers
    
    @property
    def createTime(self):
        return self.__createTime
    
    @property
    def editTime(self):
        return self.__editTime

    @property
    def isStart(self):return self.__isStart
    @isStart.setter
    def isStart(self,start:bool):self.__isStart=start

    def __init__(self, drawBoxInfo: dict=None,drawId:int=None,name: str=None,userId: str=None) -> None:
        self.__drawBoxInfo = drawBoxInfo
        
        if drawBoxInfo!=None:
            self._id = self.__drawBoxInfo[DBInfo.id.value]
            self.__name = self.__drawBoxInfo[DBInfo.dname.value]
            self.__userId = self.__drawBoxInfo[DBInfo.userId.value]
            self.__createTime=arrow.get(self.__drawBoxInfo[DBInfo.createTime.value]).datetime
            self.__editTime=arrow.get(self.__drawBoxInfo[DBInfo.editTime.value]).datetime

            self.state=StateTypes.unchanged
        else:
            self._id=drawId
            self.__name=name
            self.__userId=userId
            self.__createTime=datetime.now().replace(tzinfo=timezone(offset=timedelta()))
            self.__editTime=datetime.now().replace(tzinfo=timezone(offset=timedelta()))

            self.layers.append(Layer.create0Layer())

            self.state=StateTypes.added


    def to_dict(self) -> dict:
        return {
            DBInfo.id.value: self._id,
            DBInfo.dname.value: self.__name,
            DBInfo.userId.value: self.__userId,
            DBInfo.createTime.value:self.__createTime.isoformat(),
            DBInfo.editTime.value:self.__editTime.isoformat()
        }
