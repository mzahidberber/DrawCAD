from PyQt5.QtWidgets import QPushButton,QInputDialog
from Model import DrawBox
from Service import DrawService

class DrawBoxEditButton(QPushButton):
    def __init__(self,drawBox:DrawBox,updateFunc):
        super().__init__()
        self.__drawBox=drawBox
        self.__updateFunc=updateFunc
        self.clicked.connect(self.btnClick)

    def btnClick(self,ev):
        text, ok = QInputDialog.getText(self, 'Draw Name', self.__drawBox.name)
        if ok:
            if text!="":
                self.__drawBox.name=text
                self.__updateFunc()
