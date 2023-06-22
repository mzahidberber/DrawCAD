from Model.BaseModel import BaseModel
from Model.Color import Color
from Model.PenStyle import PenStyle
from Model.DrawEnums import PenInfo,StateTypes
import uuid

class Pen(BaseModel):
    __name: str
    __red: int
    __blue: int
    __green: int
    __penStyleId: int
    __penStyle: PenStyle or None


    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: str):
        self.__name = name
        if self.state != StateTypes.added:
            self.state = StateTypes.update
        
    @property
    def red(self):
        return self.__red

    @red.setter
    def red(self, rCode: int):
        self.__red = rCode
        if self.state != StateTypes.added:
            self.state = StateTypes.update

    @property
    def blue(self):
        return self.__blue

    @blue.setter
    def blue(self, bCode: int):
        if self.state != StateTypes.added:
            self.state = StateTypes.update
        self.__blue = bCode

    @property
    def green(self):
        return self.__green
    @green.setter
    def green(self, gCode: int):
        if self.state != StateTypes.added:
            self.state = StateTypes.update
        self.__green = gCode

    @property
    def penStyleId(self):
        return self.__penStyleId
    @penStyleId.setter
    def penStyleId(self,id:int):
        if self.state != StateTypes.added:
            self.state = StateTypes.update
        self.__penStyleId=id

    @property
    def penStyle(self):
        return self.__penStyle if self.__penStyle != None else None
    @penStyle.setter
    def penStyle(self,style:PenStyle):
        if self.state!=StateTypes.added:
            self.state=StateTypes.update
        self.__penStyle=style

    


    def __init__(self, penInfo: dict=None,id:int=0,name: str=None,penStyleId:int=None,
                 red:int=None,blue:int=None,green:int=None) -> None:
        if penInfo is not None:
            self.__penInfo = penInfo
            self._id = self.__penInfo[PenInfo.id.value]
            self.__name = self.__penInfo[PenInfo.pname.value]
            self.__penStyleId = self.__penInfo[PenInfo.penStyleId.value]
            self.__red=self.__penInfo[PenInfo.red.value]
            self.__blue=self.__penInfo[PenInfo.blue.value]
            self.__green=self.__penInfo[PenInfo.green.value]

            if self.__penInfo[PenInfo.penStyle.value] is not None:
                self.__penStyle = PenStyle(self.__penInfo[PenInfo.penStyle.value])
            else:
                self.__penStyle = None


        else:
            self._id = id
            self.__name = str(uuid.uuid4())
            self.__penStyleId = penStyleId
            self.__red=red
            self.__blue=blue
            self.__green=green

            self.__penStyle=PenStyle(name="solid")

        if self.id != 0:
            self.state = StateTypes.unchanged
        else:
            self.state = StateTypes.added

    def copy(self):return Pen(id=0,name=str(uuid.uuid4()),penStyleId=self.penStyleId,red=self.red,blue=self.blue,green=self.green)

    def to_dict_save(self) -> dict:
        return {
            PenInfo.id.value: self._id,
            PenInfo.pname.value: self.__name,
            PenInfo.penStyleId.value: self.__penStyleId,
            PenInfo.red.value:self.__red,
            PenInfo.blue.value:self.__blue,
            PenInfo.green.value:self.__green,
            PenInfo.penStyle.value:self.penStyle.to_dict()
        }
    def to_dict(self) -> dict:
        return {
            PenInfo.id.value: self._id,
            PenInfo.pname.value: self.__name,
            PenInfo.red.value:self.__red,
            PenInfo.green.value:self.__green,
            PenInfo.blue.value:self.__blue,
            PenInfo.penStyleId.value: self.__penStyleId
        }
