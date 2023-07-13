from Commands.CommandEnums import CommandEnums,CommandTypes
class Command:
    __command:CommandEnums
    __type:CommandTypes

    @property
    def command(self)->CommandEnums:return self.__command

    @property
    def type(self)->CommandTypes:return self.__type

    def __init__(self,command:CommandEnums,type:CommandTypes):
        self.__command=command
        self.__type=type