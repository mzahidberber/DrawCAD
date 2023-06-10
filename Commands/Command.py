


class Command:
    __message:str

    def __init__(self,message:str):
        self.__message=message
    @property
    def message(self)->str:return self.__message

