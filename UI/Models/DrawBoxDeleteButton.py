from PyQt5.QtWidgets import QPushButton,QMessageBox
from PyQt5.QtGui import QPixmap,QIcon,QColor
from PyQt5.QtCore import QSize
from Model import DrawBox
from Model.DrawEnums import StateTypes
from Service import DrawService


class DrawBoxDeleteButton(QPushButton):
    def __init__(self,drawBox:DrawBox,updateFunc):
        super().__init__()
        self.__drawBox=drawBox
        self.__updateFunc=updateFunc

        icon1 = QIcon()
        icon1.addPixmap(QPixmap(":/images/Images/deleteBtn.png"), QIcon.Normal, QIcon.Off)
        self.setIcon(icon1)
        self.setIconSize(QSize(27,27))
        self.setFlat(True)

        self.clicked.connect(self.btnClick)

    def btnClick(self,ev):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText("Do you want to delete the drawing?")
        msg.setWindowTitle("Delete")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
	
        returnValue = msg.exec_()

        if returnValue==QMessageBox.Ok:
            if self.__drawBox.state != StateTypes.delete:
                self.__drawBox.state=StateTypes.delete

            self.__updateFunc()


