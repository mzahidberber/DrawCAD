from PyQt5.QtGui import QPainterPath
from PyQt5.QtCore import QPointF
from Elements.ElementBuilder import ElementBuilder

from PyQt5.QtGui import QPainterPathStroker, QPainterPath
from Helpers.Settings import Setting


class LineBuilder(ElementBuilder):
    __p1: QPointF
    __p2: QPointF

    def setPointsInformation(self):
        self.__p1 = QPointF(
            self.element.points[0].pointX,
            self.element.points[0].pointY,
        )
        self.__p2 = QPointF(
            self.element.points[1].pointX,
            self.element.points[1].pointY,
        )

    def paint(self, painter):
        # painter.drawRect(self.shape().boundingRect())
        
        painter.drawLine(self.__p1, self.__p2)

    def shape(self) -> QPainterPath:
        painterStrock = QPainterPathStroker()
        painterStrock.setWidth(Setting.lineBoundDistance)
        p = QPainterPath()

        p.moveTo(self.__p1)
        p.lineTo(self.__p2)

        path1 = painterStrock.createStroke(p)
        return path1
        

    def boundaryBuild(self):
        return self.shape().boundingRect()
