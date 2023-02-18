from PyQt5.QtGui import QPainterPath
from PyQt5.QtCore import QPointF
from Elements.ElementBuilder import ElementBuilder


class LineBuilder(ElementBuilder):
    __p1:QPointF
    __p2:QPointF
    
    def setPointsInformation(self):
        self.__p1=QPointF(
            self.element.points[0].pointX,
            self.element.points[0].pointY,
            )
        self.__p2=QPointF(
            self.element.points[1].pointX,
            self.element.points[1].pointY,
            )
    
    def paint(self, painter):
        painter.drawPath(self.drawPath())
        painter.drawLine(self.__p1,self.__p2)

    def shape(self,painterPath:QPainterPath):
        painterPath.moveTo(self.__p1)
        painterPath.lineTo(self.__p2)