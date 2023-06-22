import sys
from PyQt5.QtWidgets import *
from UI import LoginView,DrawView
from UI.Models.ErrorMessageBox import ErrorMessageBox
from CrossCuttingConcers.Logging import Log
from Service.AuthService import AuthService
from Core.Internet import CheckInternet
from CrossCuttingConcers.Handling import ErrorHandle
import os
import datetime
@ErrorHandle.Error_Handler_Cls
class Run:
    @staticmethod
    def run():
        Log.log(Log.INFO, "Run App")
        app = QApplication(sys.argv)
        Run.checkInternet()
        auth = AuthService()
        window = DrawView(auth) if auth.userAndToken is not None else LoginView(auth)
        window.show()
        sys.exit(app.exec_())
    @staticmethod
    def checkInternet():
        if not CheckInternet.checkConnectInternet():
            ErrorMessageBox("You do not have an internet connection")
            sys.exit()

def checkFolders():
    folderPath = os.path.join(os.path.expanduser('~'), "Documents", "DrawProgram")
    logFolderPath = os.path.join(os.path.expanduser('~'), "Documents", "DrawProgram", "Logs")
    if not os.path.exists(folderPath):
        os.mkdir(os.path.join(os.path.expanduser('~'), "Documents", "DrawProgram"))
    if not os.path.exists(logFolderPath):
        os.mkdir(os.path.join(os.path.expanduser('~'), "Documents", "DrawProgram", "Logs"))
    settingFilePath = folderPath + "\\setting.json"
    if not os.path.exists(settingFilePath): open(settingFilePath, "w").close()
    userFilePath = folderPath + "\\user.json"
    if not os.path.exists(userFilePath): open(userFilePath, "w").close()

if __name__ == "__main__":
    checkFolders()
    Run.run()


