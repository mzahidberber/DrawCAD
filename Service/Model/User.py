

class User:
    __id:str
    __username:str
    __email:str


    @property
    def username(self):return self.__username
    @username.setter
    def username(self,username:str):self.__username=username

    @property
    def id(self):return self.__id
    @id.setter
    def id(self,id:str):self.__id=id

    @property
    def email(self):return self.__email
    @email.setter
    def email(self,email:str):self.__email=email


    def __init__(self,username:str,id:str,email:str) -> None:
        self.__email=email
        self.__id=id
        self.__username=username

    def to_Dict(self):
        return {
            "id": self.__id,
            "userName": self.__username,
            "email": self.__email
            }