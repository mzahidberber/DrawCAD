from PyQt5.QtWidgets import QMainWindow
from UI.QtUI import Ui_LoginView
from Service import DrawService, AuthService
from UI import DrawView
from CrossCuttingConcers.Logging import Log
import re
from CrossCuttingConcers.Handling.UIErrorHandle import UIErrorHandle
import requests

@UIErrorHandle.Error_Handler_Cls
class LoginView(QMainWindow):

    registerInfo:bool=False
    
    def __init__(self,auth:AuthService):
        super().__init__()
        self.ui = Ui_LoginView()
        self.ui.setupUi(self)

        self.connectButtons()

        self.ui.leUsername.hide()
        self.ui.lblUsername.hide()
        self.ui.lblEmailError.hide()
        self.ui.lblPasswordError.hide()
        self.ui.lblUsernameError.hide()

        self.__auth=auth






    
    def getInfo(self,ev):
        email=self.ui.leEmail.text()
        username=self.ui.leUsername.text()
        password=self.ui.lePassword.text()

        self.ui.lblEmailError.hide()
        self.ui.lblPasswordError.hide()
        self.ui.lblUsernameError.hide()

        if self.registerInfo==False:

            if self.checkEmail(email) and self.checkPassword(password):
                result=self.__auth.loggin(email,password)
                if result:
                    self.close()
                    self.showDrawViewWindow()
                    self.registerInfo=True
            else:
                self.ui.lbxError.setText("Email or password is not correct")

        else:
            if self.checkEmail(email) and self.checkPassword(password) and self.chenckUserName(username):
                result=self.__auth.register(username,email,password)
                if result:
                    self.ui.leUsername.hide()
                    self.ui.leEmail.setText(email)
                    self.ui.lblUsername.hide()
                    self.ui.lePassword.setText(password)
                    self.ui.btnLogin.setText("Login")
                    self.ui.btnRegister.setText("Register")
                    self.ui.lbxError.setText("Register Success!")
                    self.registerInfo=False
            else:
                self.ui.lbxError.setText("Email or username or password is not correct")


    def checkEmail(self,email:str)->bool:
        if email!="" and re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', email) and len(re.findall("\s",email))<=0 :
            self.ui.lblEmailError.hide()
            return True
        else :
            self.ui.lblEmailError.show()
            self.ui.lblEmailError.setText("Email Error!!")
            return False

    def checkPassword(self,password:str)-> bool:
        if password!="" and len(password)>=8 and len(re.findall("\d",password))>0 and len(re.findall("\s",password))<=0 and len(re.findall("[A-Z]",password))>=1 and len(re.findall("[a-z]",password))>=1:
            self.ui.lblPasswordError.hide()
            return True
        else:
            self.ui.lblPasswordError.show()
            self.ui.lblPasswordError.setText("Password Error!!")
            return False

    def chenckUserName(self,username:str)-> bool:
        if username!="" and len(username)>=8 and len(re.findall("\s",username))<=0:
            self.ui.lblUsernameError.hide()
            return True
        else:
            self.ui.lblUsernameError.show()
            self.ui.lblUsernameError.setText("Username Error!!")
            return False
    
    def register(self,ev):
        if self.registerInfo==False:
            self.ui.leUsername.show()
            self.ui.lblUsername.show()
            self.ui.btnLogin.setText("Register")
            self.ui.btnRegister.setText("SigIn")
            self.registerInfo=True
        else:
            self.ui.leUsername.hide()
            self.ui.lblUsername.hide()
            self.ui.btnLogin.setText("Login")
            self.ui.btnRegister.setText("Register")
            self.registerInfo=False

    def connectButtons(self):
        self.ui.btnLogin.clicked.connect(self.getInfo)
        self.ui.btnRegister.clicked.connect(self.register)

    def showDrawViewWindow(self):
        self.drawView = DrawView(self.__auth)
        self.drawView.show()

    

