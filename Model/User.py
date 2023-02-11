from Model.BaseModel import BaseModel
from Model.DrawEnums import UInfo
class User(BaseModel):
    __userId:int
    __userName:str
    __userPassword:str

    @property
    def userId(self):return self.__userId

    @property
    def userName(self):return self.__userName

    @property
    def userPassword(self):return self.__userPassword

    def __init__(self,userInfo:dict) -> None:
        self.__userInfo=userInfo
        self.__userId=self.__userInfo[UInfo.userId.value]
        self.__userName=self.__userInfo[UInfo.userName.value]
        self.__userPassword=self.__userInfo[UInfo.userPassword.value]

    def to_dict(self) -> dict:
        return {
            UInfo.userId.value:self.__userId,
            UInfo.userName.value:self.__userName,
            UInfo.userPassword.value:self.__userPassword
            }