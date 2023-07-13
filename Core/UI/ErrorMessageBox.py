
from PyQt5.QtWidgets import QMessageBox

class ErrorMessageBox:

    def __init__(self,msg:str,title:str=None):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        if title is not None:
            msgBox.setWindowTitle(title)
        else:
            msgBox.setWindowTitle("Error!")
        msgBox.setText(msg)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec_()