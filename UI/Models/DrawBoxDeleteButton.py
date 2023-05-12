from PyQt5.QtWidgets import QPushButton,QMessageBox
from PyQt5.QtGui import QPixmap,QIcon,QColor
from Model import DrawBox
from Model.DrawEnums import StateTypes
from Service import DrawService

class DrawBoxDeleteButton(QPushButton):
    def __init__(self,drawBox:DrawBox,updateFunc):
        super().__init__()
        self.__drawBox=drawBox
        self.__updateFunc=updateFunc

        # dltBtn.setStyleSheet(f"background-color:rgba(155, 250, 15, 1);")
        # pixmap=QPixmap(15,15)
        # pixmap.fill(QColor(255,15,154))
        # self.setMaximumSize(15,15)
        # self.setIcon(QIcon(pixmap))

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


