import sys
from PyQt5.QtWidgets import *
from UI import LoginView

app=QApplication(sys.argv)
window=LoginView()
window.show()
sys.exit(app.exec_())

""