from Helpers.Preview.BasePreview import BasePreview
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import QRectF, QPointF
from Helpers.Settings import Setting


class LinePreview(BasePreview):
    __p1: QPointF
    __p2: QPointF
    __pointList:list[QPointF]=[]
    __mousePosition:QPointF or None = None

    def setMousePosition(self,point:QPointF):self.__mousePosition=point

    def addPoint(self,point:QPointF)-> None :self.__pointList.append(point)

    def setPoints(self, points: list[QPointF]):
        self.__p1 = points[0]
        self.__p2 = points[1]

    def boundaryBuild(self):
        if (self.__mousePosition!=None and len(self.__pointList)==1):
            return QRectF(self.__p1, self.__p2)

    def paint(self, painter: QPainter):
        if (self.__mousePosition!=None and len(self.__pointList)==1):
            painter.setPen(Setting.previewLinePen)
            painter.drawLine(self.__p1, self.__p2)
        
