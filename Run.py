

import sys
from PyQt5.QtWidgets import *
from UI import LoginView,DrawView
from Core.UI.ErrorMessageBox import ErrorMessageBox
from CrossCuttingConcers.Logging import Log
from Service.AuthService import AuthService
from Core.Internet import CheckInternet
from CrossCuttingConcers.Handling import ErrorHandle
from Service.DrawService import DrawService
import os
import Version


@ErrorHandle.Error_Handler_Cls
class Run:
    @staticmethod
    def run():
        Run.checkFolders()
        Log.log(Log.INFO, "Run App")
        app = QApplication(sys.argv)
        Run.checkInternet()
        Run.checkVersion()
        auth = AuthService()
        window = DrawView(auth) if auth.userAndToken is not None else LoginView(auth)
        window.show()
        sys.exit(app.exec_())

    @staticmethod
    def checkVersion():
        auth = AuthService()
        service = DrawService(auth.userAndToken.token)
        check = service.checkVersion(Version.VERSION)
        if not check.check:
            ErrorMessageBox("The new version of the program is available. You can download it from <a href='http://drawprogram.org/'>DrawCAD</a>",title="Information")

    @staticmethod
    def checkInternet():
        if not CheckInternet.checkConnectInternet()[0]:
            ErrorMessageBox("You do not have an internet connection")
            sys.exit()

    @staticmethod
    def checkFolders():
        folderPath = os.path.join(os.path.expanduser('~'), "Documents", "DrawCAD")
        logFolderPath = os.path.join(os.path.expanduser('~'), "Documents", "DrawCAD", "Logs")
        if not os.path.exists(folderPath):
            os.mkdir(os.path.join(os.path.expanduser('~'), "Documents", "DrawCAD"))
        if not os.path.exists(logFolderPath):
            os.mkdir(os.path.join(os.path.expanduser('~'), "Documents", "DrawCAD", "Logs"))
        settingFilePath = folderPath + "\\setting.json"
        if not os.path.exists(settingFilePath): open(settingFilePath, "w").close()
        userFilePath = folderPath + "\\user.json"
        if not os.path.exists(userFilePath): open(userFilePath, "w").close()

if __name__ == "__main__":
    Run.run()


