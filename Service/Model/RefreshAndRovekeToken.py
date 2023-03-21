

class RefreshAndRovekeToken:
    __token:str


    @property
    def token(self):return self.__token
    @token.setter
    def token(self,token:str):self.__token=token


    def __init__(self,token:str) -> None:
        self.__token=token

    def to_Dict(self):
        return {
            "token": self.__token
            }