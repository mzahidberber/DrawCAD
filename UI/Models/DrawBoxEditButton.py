from PyQt5.QtWidgets import QPushButton,QInputDialog
from Model import DrawBox
from Service import DrawService
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtGui import QPixmap,QIcon
from PyQt5.QtCore import QSize

class DrawBoxEditButton(QPushButton):
    def __init__(self,drawBox:DrawBox,updateFunc):
        super().__init__()
        self.__drawBox=drawBox
        self.__updateFunc=updateFunc
        self.clicked.connect(self.btnClick)

        icon1 = QIcon()
        icon1.addPixmap(QPixmap(":/images/Images/editBtn.png"),QIcon.Normal,QIcon.Off)
        self.setIcon(icon1)
        self.setIconSize(QSize(27, 27))
        self.setFlat(True)

    def btnClick(self,ev):
        text, ok = QInputDialog.getText(self, 'Draw Name', self.__drawBox.name)
        if ok:
            if text!="":
                self.__drawBox.name=text
                self.__updateFunc()
