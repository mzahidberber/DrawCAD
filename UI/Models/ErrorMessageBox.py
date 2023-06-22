
from PyQt5.QtWidgets import QMessageBox

class ErrorMessageBox:

    def __init__(self,msg:str):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle("Error!")
        msgBox.setText(msg)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec_()