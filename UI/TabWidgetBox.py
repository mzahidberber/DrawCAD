from PyQt5.QtCore import QObject
from UI.QtUI.TabWidgetUI import Ui_TabWidget
from PyQt5.QtWidgets import QWidget

class TabWidgetBox(QWidget):
    def __init__(self,parent=None) -> None:
        super().__init__(parent=parent)
        self.ui=Ui_TabWidget()
