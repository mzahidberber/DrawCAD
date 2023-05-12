import sys
from PyQt5.QtWidgets import *
from UI import LoginView,DrawView
from CrossCuttingConcers.Logging import log
from Service.AuthService import AuthService

log("Run App")
app = QApplication(sys.argv)
auth=AuthService()
if auth.userAndToken!=None:window=DrawView(auth)
else:window = LoginView(auth)
window.show()
sys.exit(app.exec_())