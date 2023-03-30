from Model.BaseModel import BaseModel
from Model.Color import Color
from Model.PenStyle import PenStyle
from Model.DrawEnums import PenInfo,StateTypes


class Pen(BaseModel):
    __penId: int
    __penName: str
    # __penColorId: int
    # __penColor: Color or None
    __penRed: int
    __penBlue: int
    __penGreen: int
    __penStyleId: int
    __penStyle: PenStyle or None

    @property
    def penId(self):
        return self.__penId

    @property
    def penName(self):
        return self.__penName

    @penName.setter
    def penName(self, name: str):
        self.__penName = name
        self.state=StateTypes.update
        
    @property
    def penRed(self):
        return self.__penRed

    @penRed.setter
    def penRed(self, rCode: int):
        self.__penRed = rCode
        self.state=StateTypes.update

    @property
    def penBlue(self):
        return self.__penBlue

    @penBlue.setter
    def penBlue(self, bCode: int):
        self.state=StateTypes.update
        self.__penBlue = bCode

    @property
    def penGreen(self):
        return self.__penGreen
    @penGreen.setter
    def penGreen(self, gCode: int):
        self.state=StateTypes.update
        self.__penGreen = gCode

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
        self.__penId = self.__penInfo[PenInfo.penId.value]
        self.__penName = self.__penInfo[PenInfo.penName.value]
        # self.__penColorId = self.__penInfo[PenInfo.penColorId.value]
        self.__penStyleId = self.__penInfo[PenInfo.penStyleId.value]
        self.__penRed=self.__penInfo[PenInfo.penRed.value]
        self.__penBlue=self.__penInfo[PenInfo.penBlue.value]
        self.__penGreen=self.__penInfo[PenInfo.penGreen.value]

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
            PenInfo.penId.value: self.__penId,
            PenInfo.penName.value: self.__penName,
            # PenInfo.penColorId.value: self.__penColorId,
            # PenInfo.penColor.value: self.__penColor.to_dict()
            # if self.__penColor != None
            # else None,
            PenInfo.penRed.value:self.__penRed,
            PenInfo.penGreen.value:self.__penGreen,
            PenInfo.penBlue.value:self.__penBlue,
            PenInfo.penStyleId.value: self.__penStyleId,
            PenInfo.penStyle.value: self.__penStyle.to_dict()
            if self.penStyle != None
            else None,
        }
