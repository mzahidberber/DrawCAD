from PyQt5.QtGui import QPen,QColor
from PyQt5.QtCore import Qt

class CreatePen:
    
    @staticmethod
    def createPen(r:int,g:int,b:int,width:float,style) -> QPen:
        return QPen(QColor(r,g,b),width,style)