from PyQt5.QtGui import QPainterPath
from PyQt5.QtCore import QPointF
from Elements.ElementBuilder import ElementBuilder

from PyQt5.QtGui import QPainterPathStroker, QPainterPath
from Helpers.Settings import Setting

class EllipsBuilder(ElementBuilder):
    __centerPoint: QPointF
    __r1: float
    __r2: float

    def setPointsInformation(self):
        self.__centerPoint = QPointF(
            self.element.points[0].x,
            self.element.points[0].y,
        )
        self.__r1 = self.element.radiuses[0].value
        self.__r2 = self.element.radiuses[1].value

    def paint(self, painter):
        # painter.drawRect(self.shape().boundingRect())
        
        painter.drawEllipse(self.__centerPoint, self.__r1,self.__r2)

    def shape(self) -> QPainterPath:
        painterStrock = QPainterPathStroker()
        painterStrock.setWidth(Setting.lineBoundDistance)
        p = QPainterPath()

        startp=self.__centerPoint+QPointF(self.__r1,0)
        n1:QPointF=self.__centerPoint+QPointF(self.__r1,self.__r2)
        n2:QPointF=self.__centerPoint+QPointF(0,self.__r2)
        n3:QPointF=self.__centerPoint+QPointF(-self.__r1,self.__r2)
        n4:QPointF=self.__centerPoint+QPointF(-self.__r1,0)
        n5:QPointF=self.__centerPoint+QPointF(-self.__r1,-self.__r2)
        n6:QPointF=self.__centerPoint+QPointF(0,-self.__r2)
        n7:QPointF=self.__centerPoint+QPointF(self.__r1,-self.__r2)
          
        p.moveTo(startp)
        p.quadTo(n1.x(),n1.y(),n2.x(),n2.y())
        p.quadTo(n3.x(),n3.y(),n4.x(),n4.y())
        p.quadTo(n5.x(),n5.y(),n6.x(),n6.y())
        p.quadTo(n7.x(),n7.y(),startp.x(),startp.y())

        path1 = painterStrock.createStroke(p)
        return path1
        

    def boundaryBuild(self):
        return self.shape().boundingRect()
