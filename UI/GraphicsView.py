from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class GraphicsView(QGraphicsView):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.scale(1.0,-1.0)
