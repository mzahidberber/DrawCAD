from PyQt5.QtGui import QPainterPath
from PyQt5.QtCore import QPointF,QRectF
from Elements.ElementBuilder import ElementBuilder

from PyQt5.QtGui import QPainterPathStroker, QPainterPath
from Helpers.Settings import Setting

class RectangleBuilder(ElementBuilder):
    __p1: QPointF
    __p2: QPointF

    def setPointsInformation(self):
        self.__p1 = QPointF(
            self.element.points[0].x,
            self.element.points[0].y,
        )
        self.__p2 = QPointF(
            self.element.points[1].x,
            self.element.points[1].y,
        )
        self.__p3 = QPointF(
            self.element.points[2].x,
            self.element.points[2].y,
        )
        self.__p4 = QPointF(
            self.element.points[3].x,
            self.element.points[3].y,
        )

    def paint(self, painter):
        painter.drawRect(self.shape().boundingRect())
        painter.drawPath(self.shape())

        painter.drawRect(QRectF(self.__p1, self.__p2))

    def shape(self) -> QPainterPath:
        painterStrock = QPainterPathStroker()
        painterStrock.setWidth(Setting.lineBoundDistance)
        p = QPainterPath()

        p.moveTo(self.__p1)
        p.lineTo(self.__p2)
        p.lineTo(self.__p3)
        p.lineTo(self.__p4)
        p.lineTo(self.__p1)

        path1 = painterStrock.createStroke(p)
        return path1
        

    def boundaryBuild(self):
        return self.shape().boundingRect()
