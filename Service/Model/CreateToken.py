

class CreateToken:
    __password:str
    __email:str



    @property
    def password(self):return self.__password
    @password.setter
    def password(self,password:str):self.__password=password

    @property
    def email(self):return self.__email
    @email.setter
    def email(self,email:str):self.__email=email


    def __init__(self,password:str,email:str) -> None:
        self.__email=email
        self.__password=password

    def to_Dict(self):
        return {
            "email": self.__email,
            "password": self.__password
            }