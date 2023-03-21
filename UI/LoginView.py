from PyQt5.QtWidgets import QMainWindow
from UI.QtUI import Ui_LoginView
from Service import DrawService, AuthService
from UI import DrawView
from CrossCuttingConcers.Logging import log
import json
from Service.Model.Token import Token


class LoginView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_LoginView()
        self.ui.setupUi(self)

        self.connectButtons()

        self.__auth=AuthService("zahid@gmail.com", "123456Aa")

        self.drawBoxView = None
        self.drawView = None

        self.loggin()

    def loggin(self):
        self.close()
        self.showDrawViewWindow()

    def connectButtons(self):pass
        # self.ui.btnLogin.clicked.connect(self.loggin)
        # self.ui.btnRegister.clicked.connect(self.register)

    def showDrawViewWindow(self):
        if self.drawView == None:
            self.drawView = DrawView(self.__auth.userAndToken.token)
        self.drawView.show()

    

