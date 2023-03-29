from Commands import CommandPanel
from Model import DrawBox


class DrawBoxObj:
    __drawBox:DrawBox
    __commandPanel:CommandPanel

    @property
    def commandPanel(self) -> CommandPanel:return self.__commandPanel

    @property
    def drawBox(self) -> DrawBox:return self.__drawBox

    def __init__(self,commandPanel:CommandPanel) -> None:
        self.__commandPanel=commandPanel
        self.__drawBox=commandPanel.drawBox