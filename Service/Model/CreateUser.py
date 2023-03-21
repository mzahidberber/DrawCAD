
class CreateUser:
    __username:str
    __password:str
    __email:str


    @property
    def username(self):return self.__username
    @username.setter
    def username(self,username:str):self.__username=username

    @property
    def password(self):return self.__password
    @password.setter
    def password(self,password:str):self.__password=password

    @property
    def email(self):return self.__email
    @email.setter
    def email(self,email:str):self.__email=email


    def __init__(self,username:str,password:str,email:str) -> None:
        self.__email=email
        self.__password=password
        self.__username=username

    def to_Dict(self):
        return {
            "userName": self.__username,
            "email": self.__email,
            "password": self.__password
            }