from PyQt5.QtWidgets import QMainWindow
from UI.QtUI import Ui_LoginView
from Service import DrawService
from UI import DrawView

class UserInfo:
    username="zahid"
    password="123456"
class LoginView(QMainWindow):
    def __init__(self):
        super(LoginView,self).__init__()
        self.ui=Ui_LoginView()
        self.ui.setupUi(self)

        self.connectButtons()
        
        self.username=""
        self.password=""

        self.drawBoxView=None
        self.drawView=None

        self.loggin()
        
    def loggin(self):
        DrawService().login("zahid","123456")
        self.close()
        self.showDrawViewWindow()
    
    def connectButtons(self):
        self.ui.btnLogin.clicked.connect(self.login)
        self.ui.btnRegister.clicked.connect(self.register)


    def showDrawViewWindow(self):
        if self.drawView == None:
            self.drawView=DrawView()
        self.drawView.show()

    def login(self):
        self.username=self.ui.leUsername.text()
        self.password=self.ui.lePassword.text()
        result=DrawService().login(self.username,self.password)
        print(type(result))
        try:
            resultt=result.json()
            if resultt["login"]==True:
                self.close()
                self.showDrawViewWindow()
                
        except:
            print(result.text)

    def register(self):pass