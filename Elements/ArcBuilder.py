from PyQt5.QtGui import QPainterPath
from PyQt5.QtCore import QPointF,QRectF
from Elements.ElementBuilder import ElementBuilder
from Helpers.GeoMath import GeoMath

from PyQt5.QtGui import QPainterPathStroker, QPainterPath
from Helpers.Settings import Setting
class ArcBuilder(ElementBuilder):
    def setPointsInformation(self):
        self.__firstPoint=self.element.points[1]
        self.__centerPoint=self.element.points[0]
        self.__radius=self.element.radiuses[0].value
        self.__startAngle=self.element.ssAngles[0].value
        self.__stopAngle=self.element.ssAngles[1].value

        self.__square=QRectF(
            QPointF(self.__centerPoint.x-self.__radius,self.__centerPoint.y-self.__radius),
            QPointF(self.__centerPoint.x+self.__radius,self.__centerPoint.y+self.__radius))

    def paint(self, painter):
        painter.drawArc(self.__square,int(self.__startAngle),int(self.__stopAngle))
        # painter.drawPath(self.shape())
        # painter.drawRect(self.shape().boundingRect())

    def shape(self) -> QPainterPath:
        painterStrock = QPainterPathStroker()
        painterStrock.setWidth(Setting.lineBoundDistance)
        p = QPainterPath()

        p.moveTo(QPointF(self.__firstPoint.x,self.__firstPoint.y))
        p.arcTo(self.__square,int(self.__startAngle/16),int(self.__stopAngle/16))

        path1 = painterStrock.createStroke(p)
        return path1

    def boundaryBuild(self):
        return self.shape().boundingRect()
