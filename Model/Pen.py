from Model.BaseModel import BaseModel
from Model.Color import Color
from Model.PenStyle import PenStyle
from Model.DrawEnums import PenInfo,StateTypes


class Pen(BaseModel):
    __name: str
    # __penColorId: int
    # __penColor: Color or None
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
        self.state=StateTypes.update
        
    @property
    def red(self):
        return self.__red

    @red.setter
    def red(self, rCode: int):
        self.__red = rCode
        self.state=StateTypes.update

    @property
    def blue(self):
        return self.__blue

    @blue.setter
    def blue(self, bCode: int):
        self.state=StateTypes.update
        self.__blue = bCode

    @property
    def green(self):
        return self.__green
    @green.setter
    def green(self, gCode: int):
        self.state=StateTypes.update
        self.__green = gCode

    # @property
    # def penColorId(self):
    #     return self.__penColorId

    # @property
    # def penColor(self):
    #     return self.__penColor if self.__penColor != None else None

    @property
    def penStyleId(self):
        return self.__penStyleId
    @penStyleId.setter
    def penStyleId(self,id:int):
        self.state=StateTypes.update
        self.__penStyleId=id

    @property
    def penStyle(self):
        return self.__penStyle if self.__penStyle != None else None
    @penStyle.setter
    def penStyle(self,style:PenStyle):
        self.state=StateTypes.update
        self.__penStyle=style

    


    def __init__(self, penInfo: dict) -> None:
        self.__penInfo = penInfo
        self._id = self.__penInfo[PenInfo.id.value]
        self.__name = self.__penInfo[PenInfo.pname.value]
        # self.__penColorId = self.__penInfo[PenInfo.penColorId.value]
        self.__penStyleId = self.__penInfo[PenInfo.penStyleId.value]
        self.__red=self.__penInfo[PenInfo.red.value]
        self.__blue=self.__penInfo[PenInfo.blue.value]
        self.__green=self.__penInfo[PenInfo.green.value]

        # if self.__penInfo[PenInfo.penColor.value] != None:
        #     self.__penColor = Color(self.__penInfo[PenInfo.penColor.value])
        # else:
        #     self.__penColor = None



        if self.__penInfo[PenInfo.penStyle.value] != None:
            self.__penStyle = PenStyle(self.__penInfo[PenInfo.penStyle.value])
        else:
            self.__penStyle = None



        self.state=StateTypes.unchanged

    def to_dict(self) -> dict:
        return {
            PenInfo.id.value: self._id,
            PenInfo.pname.value: self.__name,
            # PenInfo.penColorId.value: self.__penColorId,
            # PenInfo.penColor.value: self.__penColor.to_dict()
            # if self.__penColor != None
            # else None,
            PenInfo.red.value:self.__red,
            PenInfo.green.value:self.__green,
            PenInfo.blue.value:self.__blue,
            PenInfo.penStyleId.value: self.__penStyleId,
            PenInfo.penStyle.value: self.__penStyle.to_dict()
            if self.penStyle != None
            else None,
        }
