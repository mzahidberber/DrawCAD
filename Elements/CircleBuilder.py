from PyQt5.QtGui import QPainterPath
from PyQt5.QtCore import QPointF, QRectF
from Elements.ElementBuilder import ElementBuilder


class CircleBuilder(ElementBuilder):
    __center: QPointF
    __radius: float
    __p1: QPointF
    __p2: QPointF
    __p3: QPointF
    __p4: QPointF

    def setPointsInformation(self):
        self.__center = QPointF(
            self.element.points[0].pointX, self.element.points[0].pointY
        )

        self.__radius = self.element.radiuses[0].radiusValue

        # if self.element.points[1].pointX-self.__center.x()!=self.element.radiuses[0].radiusValue:
        #     self.element.radiuses[0].radiusValue=self.element.points[1].pointX-self.__center.x()

        self.__p1 = QPointF(
            self.element.points[1].pointX, self.element.points[1].pointY
        )
        self.__p2 = QPointF(
            self.element.points[2].pointX, self.element.points[2].pointY
        )
        self.__p3 = QPointF(
            self.element.points[3].pointX, self.element.points[3].pointY
        )
        self.__p4 = QPointF(
            self.element.points[4].pointX, self.element.points[4].pointY
        )

    def paint(self, painter):
        painter.drawEllipse(self.__center, self.__radius, self.__radius)
        painter.drawPath(self.drawPath())

    def shape(self, painterPath: QPainterPath):
        startP = self.__center + QPointF(self.__radius, 0)
        painterPath.moveTo(startP)
        squareStartP = self.__center - QPointF(self.__radius, self.__radius)
        squareStopP = self.__center + QPointF(self.__radius, self.__radius)
        square = QRectF(squareStartP, squareStopP)
        painterPath.arcTo(square, 0, 360)
