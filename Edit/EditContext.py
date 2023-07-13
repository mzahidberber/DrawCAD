from Edit.Move import Move
from Edit.BaseEdit import BaseEdit
from Helpers.Select import Select
from Helpers.Snap import Snap
from Edit.Copy import Copy
from Edit.Rotate import Rotate
from Edit.Scale import Scale
from Edit.Mirror import Mirror
class EditContext:
    __editCommandType: BaseEdit or None=None
    __editCommand:BaseEdit
    __editTypes: dict = {
        8: Move,
        9: Copy,
        12:Rotate,
        13:Scale,
        14:Mirror
    }

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(EditContext, cls).__new__(cls)
        return cls.instance

    def setEditCommand(self, editType: int,commandPanel) -> BaseEdit:
        self.__editCommandType = self.__editTypes[editType]
        self.__editCommand=self.__editCommandType(commandPanel)
        return self.__editCommand

    def stopEditCommand(self):self.__editCommandType=None

    def getEditCommand(self)-> BaseEdit:return self.__editCommand if self.__editCommandType is not None else None