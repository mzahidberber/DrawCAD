from Helpers.Preview.BasePreview import BasePreview
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import QRectF,QPointF
from Helpers.Settings import Setting

class LinePreview(BasePreview):
    __p1:QPointF
    __p2:QPointF

    def setPoints(self,points:list[QPointF]):
        self.__p1=points[0]
        self.__p2=points[1]
    
    def boundaryBuild(self):return QRectF(self.__p1,self.__p2)

    def paint(self,painter:QPainter):
        painter.setPen(Setting.previewLinePen)
        painter.drawLine(self.__p1,self.__p2)